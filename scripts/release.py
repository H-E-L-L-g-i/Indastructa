import argparse
import sys
from pathlib import Path
import textwrap
import re
from typing import Optional

import requests
import toml

# --- Configuration ---
PYPROJECT_PATH = Path(__file__).parent.parent / "pyproject.toml"
DEFAULT_PYPI_REPO = "testpypi"
PYPI_URLS = {
    "pypi": "https://pypi.org/pypi/{package_name}/{version}/json",
    "testpypi": "https://test.pypi.org/pypi/{package_name}/{version}/json",
}
VERSION_REGEX_PATTERN = r"^(\d+)\.(\d+)\.(\d+)(?:\.dev(\d+))?$"


def get_project_info() -> tuple[str, str]:
    """Reads package name and version from pyproject.toml."""
    if not PYPROJECT_PATH.is_file():
        print(f"Error: pyproject.toml not found at {PYPROJECT_PATH}")
        sys.exit(1)
    config = toml.load(PYPROJECT_PATH)
    name = config.get("project", {}).get("name")
    version = config.get("project", {}).get("version")
    if not name or not version:
        print(
            "Error: 'name' or 'version' not found in [project] section "
            " of 'pyproject.toml' file")
        sys.exit(1)
    return name, version


def validate_version_string(version: str) -> bool:
    """
    Validates a version string against a standard format.
    """
    return re.match(VERSION_REGEX_PATTERN, version) is not None


def parse_version(version: str) -> tuple[int, int, int, Optional[int]]:
    """Parses a version string into its components."""
    match = re.match(VERSION_REGEX_PATTERN, version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch = map(int, match.groups()[:3])
    dev_number = int(match.group(4)) if match.group(4) else None
    return major, minor, patch, dev_number


def check_if_version_exists(package_name: str, version: str, repo: str) -> bool:
    """
    Checks if a version of the package already exists on the specified repository.
    """
    if not validate_version_string(version):
        raise ValueError(f"Incorrect version format: '{version}'. "
                         f"Must be 'X.Y.Z' or 'X.Y.Z.devN'")

    url = PYPI_URLS[repo].format(package_name=package_name, version=version)
    print(f"Checking for version {version} on {repo.upper()}...")
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Warning: Could not check version on {repo.upper()}: {e}")
        return False


def bump_version(current_version: str, part: Optional[str] = None, bump_dev: bool = False) -> str:
    """Bumps the version string based on the specified part."""
    major, minor, patch, dev_number = parse_version(current_version)

    match part:
        case "major":
            major += 1
            minor = patch = 0
        case "minor":
            minor += 1
            patch = 0
        case "patch":
            patch += 1
        case None:
            if bump_dev:
                dev_number = 1 if dev_number is None else dev_number + 1
                return f"{major}.{minor}.{patch}.dev{dev_number}"
            else:
                raise ValueError("You must specify a version part ('major', 'minor', 'patch') "
                                 "or use --dev to bump a dev version.")
        case _:
            raise ValueError(f"Unknown version part: {part}")

    if bump_dev:
        return f"{major}.{minor}.{patch}.dev1"
    return f"{major}.{minor}.{patch}"


def update_pyproject_toml(new_version: str):
    """Updates the version in the pyproject.toml file."""
    print(f"Updating pyproject.toml to version {new_version}...")
    config = toml.load(PYPROJECT_PATH)
    config["project"]["version"] = new_version
    with open(PYPROJECT_PATH, "w") as f:
        toml.dump(config, f)
    print("pyproject.toml updated successfully.")


def print_release_instructions(version: str):
    """Prints the final git commands for the user to run."""
    instructions = f"""{"\n" + "=" * 60}
NEXT STEPS: Manually create the release commit and tag.
Run the following commands:

    git add pyproject.toml
    git commit -m "chore: Prepare release v{version}"
    git tag v{version}

    git push && git push origin v{version}{"=" * 60}
"""
    print(instructions)


def parse_cli_args(script_name: str):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="A script to check and bump the project version for a release.",
        epilog=textwrap.dedent(f"""
            Examples:
              # 1. Check the current version against TestPyPI
              python scripts/{script_name}

              # 2. Bump the patch version and check against the official PyPI
              python scripts/{script_name} patch --repo pypi

              # 3. Bump minor and start a dev version
              python scripts/{script_name} minor --dev
              
              # 4. Perform a dry run to see the new version without changing any files
              python scripts/{script_name} patch --dry-run
        """),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "part", nargs="?", choices=["major", "minor", "patch"],
        help="Optional. The part of the version to increment."
    )
    parser.add_argument(
        "--repo", choices=["pypi", "testpypi"], default=DEFAULT_PYPI_REPO,
        help=f"The repository to check the version against. Defaults to '{DEFAULT_PYPI_REPO}'."
    )
    parser.add_argument(
        "--dev", action="store_true",
        help="If the current version is a dev version, increment the dev number."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Perform a trial run without changing any files."
    )
    return parser.parse_args()


def determine_new_version(current_version: str, part: Optional[str], bump_dev: bool) -> str:
    """Decides what the new version should be based on CLI arguments."""
    if not part and bump_dev:
        return bump_version(current_version, part=None, bump_dev=True)
    return bump_version(current_version, part=part, bump_dev=bump_dev)


def check_version_availability(package_name: str, version: str, repo: str):
    """Checks if the version exists on the repo and exits if it does."""
    try:
        if check_if_version_exists(package_name, version, repo):
            print(f"Error: Version {version} already exists on {repo.upper()}. Please check manually.")
            sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def handle_bump_scenario(args, package_name, current_version):
    """Handles the logic for bumping a version."""
    new_version = determine_new_version(current_version, args.part, args.dev)
    print(f"New version would be: {new_version}")

    check_version_availability(package_name, new_version, args.repo)
    print(f"Version {new_version} is available on {args.repo.upper()}.")

    if args.dry_run:
        print("Would prompt to update pyproject.toml.")
        print("-- END DRY RUN --")
        return

    confirm = input(f"Update pyproject.toml to version {new_version}? (y/n): ")
    if confirm.lower() == 'y':
        update_pyproject_toml(new_version)
        print_release_instructions(new_version)
    else:
        print("Aborted by user.")


def handle_check_scenario(args, package_name, current_version):
    """Handles the logic for checking the current version."""
    check_version_availability(package_name, current_version, args.repo)
    print(f"Version {current_version} is available on {args.repo.upper()}.")

    if args.dry_run:
        print("Would prompt to prepare a release for this version.")
        print("-- END DRY RUN --")
        return

    confirm = input(f"\nDo you want to prepare a release for this version ('{current_version}')? (y/n): ")
    if confirm.lower() == 'y':
        print_release_instructions(current_version)
    else:
        print("Aborted by user.")


def main():
    """Main script logic."""
    script_name = Path(__file__).name
    args = parse_cli_args(script_name)
    package_name, current_version = get_project_info()
    print(f"Package: {package_name}")
    print(f"Current version in 'pyproject.toml' file: {current_version}")

    if args.dry_run:
        print("\n-- DRY RUN MODE --")

    if args.part or args.dev:
        handle_bump_scenario(args, package_name, current_version)
    else:
        handle_check_scenario(args, package_name, current_version)


if __name__ == "__main__":
    main()
