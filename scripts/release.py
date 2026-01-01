import argparse
import sys
from pathlib import Path
import textwrap
import re
import subprocess
from typing import Optional

import requests
import toml

# --- Configuration ---
PYPROJECT_PATH = Path(__file__).parent.parent / "pyproject.toml"
CHANGELOG_PATH = Path(__file__).parent.parent / "CHANGELOG.md"
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


def bump_version_string(current_version: str, part: str) -> str:
    """Bumps the version string based on the specified part."""
    match = re.match(VERSION_REGEX_PATTERN, current_version)
    if not match:
        print(f"Error: Invalid version format: {current_version}")
        sys.exit(1)
        
    major, minor, patch = map(int, match.groups()[:3])

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print(f"Error: Unknown version part: {part}")
        sys.exit(1)
        
    return f"{major}.{minor}.{patch}"


def update_pyproject_toml(new_version: str):
    """Updates the version in the pyproject.toml file."""
    print(f"Updating pyproject.toml to version {new_version}...")
    config = toml.load(PYPROJECT_PATH)
    config["project"]["version"] = new_version
    with open(PYPROJECT_PATH, "w") as f:
        toml.dump(config, f)
    print("pyproject.toml updated successfully.")


def run_command(command: list, error_msg: str):
    """Runs a command and exits on error."""
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_msg}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)


def main():
    """Main script logic."""
    parser = argparse.ArgumentParser(description="Prepares a new release by updating version, creating a commit and a tag.")
    parser.add_argument("part", choices=["major", "minor", "patch"], help="The part of the version to increment.")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompts.")
    args = parser.parse_args()

    # --- Pre-flight checks ---
    print("Performing pre-flight checks...")
    if subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout:
        print("Error: Your working directory is not clean. Please commit or stash your changes.")
        sys.exit(1)

    current_branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
    if current_branch != "main" and not args.yes:
        print(f"Warning: You are on branch '{current_branch}', not 'main'.")
        if input("Continue anyway? (y/N): ").lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    # --- Planning ---
    current_version = get_project_info()[1]
    new_version = bump_version_string(current_version, args.part)
    tag_name = f"v{new_version}"

    print("\nRelease Plan:")
    print(f"  - Current version: {current_version}")
    print(f"  - New version:     {new_version}")
    print(f"  - Tag to create:   {tag_name}")

    if not args.yes and input("\nProceed with these actions? (y/N): ").lower() != 'y':
        print("Aborted.")
        sys.exit(0)

    # --- Execution ---
    print("\nExecuting release...")
    update_pyproject_toml(new_version)
    
    print("Creating release commit and tag...")
    run_command(["git", "add", str(PYPROJECT_PATH)], "Failed to stage pyproject.toml")
    
    commit_message = f"chore: Release {tag_name}"
    run_command(["git", "commit", "-m", commit_message], "Failed to create commit")

    # Check if tag already exists before creating
    existing_tags = subprocess.run(["git", "tag"], capture_output=True, text=True).stdout.splitlines()
    if tag_name in existing_tags:
        print(f"Warning: Tag {tag_name} already exists. Skipping tag creation.")
    else:
        run_command(["git", "tag", tag_name], f"Failed to create tag {tag_name}")

    print("\nDone.")
    print("NEXT STEP: Push the commit and tag to trigger the release workflow:")
    print("\n    git push && git push --tags\n")


if __name__ == "__main__":
    main()
