"""
This test module is intended to be run in a CI/CD environment ONLY.
It performs a live check against a PyPI repository to ensure a version
does not already exist before a publication attempt.
"""

import os
import pytest
import requests
import toml
from pathlib import Path

# --- Configuration ---
# This check only runs if this environment variable is set to 'true'
RUN_RELEASE_CHECK = os.environ.get("CI_RELEASE_CHECK", "false").lower() == "true"

# The target repository ('pypi' or 'testpypi') is also determined by an environment variable.
PYPI_TARGET = os.environ.get("PYPI_TARGET", "testpypi")
PYPI_URLS = {
    "pypi": "https://pypi.org/pypi/{package_name}/{version}/json",
    "testpypi": "https://test.pypi.org/pypi/{package_name}/{version}/json",
}


# --- Helper function to get project info ---
def get_project_info() -> tuple[str, str]:
    """Reads package name and version from the project's pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if not pyproject_path.is_file():
        pytest.fail(f"pyproject.toml not found at {pyproject_path}")

    config = toml.load(pyproject_path)
    name = config.get("project", {}).get("name")
    version = config.get("project", {}).get("version")

    if not name or not version:
        pytest.fail("Could not find 'name' or 'version' in pyproject.toml")

    return name, version


# --- The Test ---


@pytest.mark.network
def test_version_is_not_published():
    """
    Checks that the current project version does not already exist on the target PyPI repository.
    This test is skipped unless the CI_RELEASE_CHECK environment variable is set to 'true'.
    """
    if not RUN_RELEASE_CHECK:
        pytest.skip(
            "Skipping live PyPI release check. This test is intended for the CI/CD release workflow only."
        )

    package_name, version = get_project_info()
    url = PYPI_URLS[PYPI_TARGET].format(package_name=package_name, version=version)

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        pytest.skip(f"Could not connect to {PYPI_TARGET}. Skipping test. Reason: {e}")

    # If status code is 200, the version exists, and the test should fail.
    if response.status_code == 200:
        pytest.fail(
            f"\n"
            f"---------------------------- RELEASE CHECK FAILED ----------------------------\n"
            f"Reason:  Version {version} of package '{package_name}' already exists on {PYPI_TARGET.upper()}.\n"
            f"Action:  Please increment the version in 'pyproject.toml' before releasing.\n"
            f"URL:     {url}\n"
            f"-----------------------------------------------------------------------------"
        )

    # Any other status code (like 404) means the version does not exist, which is what we want.
    print(f"Success: Version {version} is available on {PYPI_TARGET.upper()}.")
