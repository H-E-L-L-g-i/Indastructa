import pytest
import toml
from pathlib import Path

# Path to the temporary pyproject.toml
TEMP_PYPROJECT_PATH = Path("temp_pyproject.toml")


@pytest.fixture
def temp_pyproject_toml():
    """
    Creates a temporary pyproject.toml file for testing and ensures it's cleaned up.
    """
    original_pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"

    # Save the original path
    original_pyproject_path_backup = original_pyproject_path

    # Point the script's configuration to the temporary file
    # This is a bit of a hack, but necessary for isolated testing
    import sys

    sys.modules["release"].PYPROJECT_PATH = TEMP_PYPROJECT_PATH

    # Create a simple, temporary pyproject.toml for the test
    test_config = {"project": {"name": "test-package", "version": "1.0.0"}}
    with open(TEMP_PYPROJECT_PATH, "w") as f:
        toml.dump(test_config, f)

    yield TEMP_PYPROJECT_PATH

    # Clean up the temporary file and restore the original path
    if TEMP_PYPROJECT_PATH.exists():
        TEMP_PYPROJECT_PATH.unlink()

    # Restore the original path
    sys.modules["release"].PYPROJECT_PATH = original_pyproject_path_backup
