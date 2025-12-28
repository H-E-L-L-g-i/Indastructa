import pytest
import sys
from unittest.mock import patch, MagicMock, ANY
from pathlib import Path
import toml
import argparse

# Add the parent directory to the path so we can import the release script
sys.path.append(str(Path(__file__).parent.parent))

# Import the script to be tested
import release as r


@pytest.fixture(autouse=True)
def mock_pyproject_path(tmp_path):
    """
    Fixture to mock the PYPROJECT_PATH in the release script.
    """
    mock_path = tmp_path / "pyproject.toml"
    with patch("release.PYPROJECT_PATH", new=mock_path):
        yield mock_path


def test_get_project_info_success(mock_pyproject_path):
    """
    Test successful retrieval of project info from a mock pyproject.toml.
    """
    mock_pyproject_path.write_text("[project]\nname = 'my-package'\nversion = '1.2.3'")
    name, version = r.get_project_info()
    assert name == "my-package"
    assert version == "1.2.3"


def test_get_project_info_missing_fields(mock_pyproject_path):
    """
    Test handling of a missing 'name' or 'version' field.
    """
    mock_pyproject_path.write_text("[project]\nname = 'my-package'")
    with pytest.raises(SystemExit):
        r.get_project_info()


@pytest.mark.parametrize("version, expected", [
    ("1.2.3", True),
    ("1.2.3.dev4", True),
    ("1.2", False),
    ("1.2.3.dev", False),
    ("1.2.3a", False),
])
def test_validate_version_string(version, expected):
    """
    Test version string validation with various formats.
    """
    assert r.validate_version_string(version) == expected


@pytest.mark.parametrize("version, expected_parts", [
    ("1.2.3", (1, 2, 3, None)),
    ("10.20.30", (10, 20, 30, None)),
    ("1.2.3.dev4", (1, 2, 3, 4)),
])
def test_parse_version_success(version, expected_parts):
    """
    Test successful parsing of valid version strings.
    """
    assert r.parse_version(version) == expected_parts


@pytest.mark.parametrize("version", ["1.2", "abc", "1.2.3dev"])
def test_parse_version_invalid(version):
    """
    Test that parsing an invalid version string raises a ValueError.
    """
    with pytest.raises(ValueError):
        r.parse_version(version)


@patch("requests.get")
def test_check_if_version_exists_200(mock_get):
    """
    Test when a version already exists (status code 200).
    """
    mock_get.return_value.status_code = 200
    assert r.check_if_version_exists("test-package", "1.0.0", "pypi") is True


@patch("requests.get")
def test_check_if_version_exists_404(mock_get):
    """
    Test when a version does not exist (status code 404).
    """
    mock_get.return_value.status_code = 404
    assert r.check_if_version_exists("test-package", "1.0.0", "pypi") is False


@patch("requests.get", side_effect=r.requests.RequestException)
def test_check_if_version_exists_request_exception(mock_get, capsys):
    """
    Test handling of a network or request exception.
    """
    assert r.check_if_version_exists("test-package", "1.0.0", "pypi") is False
    captured = capsys.readouterr()
    assert "Warning: Could not check version on PYPI:" in captured.out


@pytest.mark.parametrize("current, part, dev, expected", [
    ("1.0.0", "major", False, "2.0.0"),
    ("1.2.3", "minor", False, "1.3.0"),
    ("1.2.3", "patch", False, "1.2.4"),
    ("1.2.3", "major", True, "2.0.0.dev1"),
    ("1.2.3", "minor", True, "1.3.0.dev1"),
    ("1.2.3", "patch", True, "1.2.4.dev1"),
    ("1.2.3.dev4", "major", False, "2.0.0"),
    ("1.2.3.dev4", "minor", False, "1.3.0"),
    ("1.2.3.dev4", "patch", False, "1.2.4"),
    ("1.2.3.dev4", "patch", True, "1.2.4.dev1"),
    ("1.2.3.dev4", None, True, "1.2.3.dev5"),
    ("1.2.3", None, True, "1.2.3.dev1"),
])
def test_bump_version_all_cases(current, part, dev, expected):
    """
    Test the bump_version function with various scenarios.
    """
    if part is None and not dev:
        with pytest.raises(ValueError,
                           match="You must specify a version part"):
            r.bump_version(current, part=part, bump_dev=dev)
    else:
        assert r.bump_version(current, part=part, bump_dev=dev) == expected


def test_update_pyproject_toml(mock_pyproject_path):
    """
    Test that the pyproject.toml file is correctly updated.
    """
    # Create the temporary file with a dummy content
    initial_content = {
        "project": {
            "name": "test-package",
            "version": "1.0.0"
        }
    }
    with open(mock_pyproject_path, "w") as f:
        toml.dump(initial_content, f)

    # Now call the function that will modify the file
    r.update_pyproject_toml("2.0.0")

    # Read the updated file and check the version
    updated_config = toml.load(mock_pyproject_path)
    assert updated_config["project"]["version"] == "2.0.0"


def test_print_release_instructions_output(capsys):
    """
    Test that the correct release instructions are printed.
    """
    version = "1.2.3"
    r.print_release_instructions(version)
    captured = capsys.readouterr()

    # Check that the most important parts are in the captured output
    assert "NEXT STEPS: Manually create the release commit and tag." in captured.out
    assert '    git add pyproject.toml' in captured.out
    assert f'    git commit -m "chore: Prepare release v{version}"' in captured.out
    assert f'    git tag v{version}' in captured.out
    assert f'    git push && git push origin v{version}' in captured.out


@patch("release.sys.exit")
@patch("release.check_if_version_exists", MagicMock(return_value=True))
def test_check_version_availability_exists(mock_exit):
    """
    Test that the function exits when the version already exists.
    """
    r.check_version_availability("test-package", "1.0.0", "pypi")
    mock_exit.assert_called_with(1)

# ============================================================================
# CRITICAL BUG TEST - Added after code review
# ============================================================================

def test_determine_new_version_dev_only():
    """
    CRITICAL TEST: Verifies that --dev without part does dev-only bump.
    """
    result = r.determine_new_version("1.0.0", part=None, bump_dev=True)
    assert result == "1.0.0.dev1"

def test_determine_new_version_with_part():
    """Test determine_new_version when part is specified."""
    result = r.determine_new_version("1.0.0", part="patch", bump_dev=False)
    assert result == "1.0.1"

# ============================================================================
# UNIT TESTS for helpers
# ============================================================================

@patch("release.print_release_instructions")
@patch("release.update_pyproject_toml")
@patch("builtins.input", return_value="y")
@patch("release.check_version_availability")
def test_handle_bump_scenario_yes(mock_check, mock_input, mock_update, mock_print, monkeypatch):
    """Test the bump scenario when user confirms."""
    args = argparse.Namespace(part="patch", dev=False, dry_run=False, repo="testpypi")
    r.handle_bump_scenario(args, "my-package", "1.0.0")
    
    mock_check.assert_called_once_with("my-package", "1.0.1", "testpypi")
    mock_input.assert_called_once()
    mock_update.assert_called_once_with("1.0.1")
    mock_print.assert_called_once_with("1.0.1")

@patch("release.print_release_instructions")
@patch("release.update_pyproject_toml")
@patch("builtins.input", return_value="n")
@patch("release.check_version_availability")
def test_handle_bump_scenario_no(mock_check, mock_input, mock_update, mock_print, monkeypatch):
    """Test the bump scenario when user aborts."""
    args = argparse.Namespace(part="patch", dev=False, dry_run=False, repo="testpypi")
    r.handle_bump_scenario(args, "my-package", "1.0.0")
    
    mock_check.assert_called_once()
    mock_input.assert_called_once()
    mock_update.assert_not_called()
    mock_print.assert_not_called()

@patch("release.print_release_instructions")
@patch("release.update_pyproject_toml")
@patch("builtins.input")
@patch("release.check_version_availability")
def test_handle_bump_scenario_dry_run(mock_check, mock_input, mock_update, mock_print, monkeypatch):
    """Test the bump scenario with --dry-run."""
    args = argparse.Namespace(part="patch", dev=False, dry_run=True, repo="testpypi")
    r.handle_bump_scenario(args, "my-package", "1.0.0")
    
    mock_check.assert_called_once()
    mock_input.assert_not_called()
    mock_update.assert_not_called()
    mock_print.assert_not_called()

@patch("release.print_release_instructions")
@patch("builtins.input", return_value="y")
@patch("release.check_version_availability")
def test_handle_check_scenario_yes(mock_check, mock_input, mock_print):
    """Test the check scenario when user confirms."""
    args = argparse.Namespace(dry_run=False, repo="testpypi")
    r.handle_check_scenario(args, "my-package", "1.0.0")

    mock_check.assert_called_once_with("my-package", "1.0.0", "testpypi")
    mock_input.assert_called_once()
    mock_print.assert_called_once_with("1.0.0")

@patch("release.print_release_instructions")
@patch("builtins.input", return_value="n")
@patch("release.check_version_availability")
def test_handle_check_scenario_no(mock_check, mock_input, mock_print):
    """Test the check scenario when user aborts."""
    args = argparse.Namespace(dry_run=False, repo="testpypi")
    r.handle_check_scenario(args, "my-package", "1.0.0")

    mock_check.assert_called_once()
    mock_input.assert_called_once()
    mock_print.assert_not_called()

@patch("release.print_release_instructions")
@patch("builtins.input")
@patch("release.check_version_availability")
def test_handle_check_scenario_dry_run(mock_check, mock_input, mock_print):
    """Test the check scenario with --dry-run."""
    args = argparse.Namespace(dry_run=True, repo="testpypi")
    r.handle_check_scenario(args, "my-package", "1.0.0")

    mock_check.assert_called_once()
    mock_input.assert_not_called()
    mock_print.assert_not_called()

# ============================================================================
# INTEGRATION TESTS for main()
# ============================================================================

class TestMainIntegration:
    @patch("release.requests.get")
    @patch("builtins.input", return_value="y")
    def test_main_scenario_patch_bump(self, mock_input, mock_get, mock_pyproject_path, monkeypatch):
        """
        Integration test for a full 'patch' bump scenario.
        `python release.py patch`
        """
        mock_pyproject_path.write_text("[project]\nname = 'my-package'\nversion = '1.0.0'")
        mock_get.return_value.status_code = 404
        monkeypatch.setattr(sys, "argv", ["release.py", "patch"])

        r.main()

        updated_config = toml.load(mock_pyproject_path)
        assert updated_config["project"]["version"] == "1.0.1"

    @patch("release.requests.get")
    @patch("builtins.input", return_value="y")
    def test_main_scenario_dev_only_bump(self, mock_input, mock_get, mock_pyproject_path, monkeypatch):
        """
        Integration test for a dev-only bump.
        `python release.py --dev`
        """
        mock_pyproject_path.write_text("[project]\nname = 'my-package'\nversion = '1.0.0'")
        mock_get.return_value.status_code = 404
        monkeypatch.setattr(sys, "argv", ["release.py", "--dev"])

        r.main()

        updated_config = toml.load(mock_pyproject_path)
        assert updated_config["project"]["version"] == "1.0.0.dev1"

    @patch("release.requests.get")
    @patch("builtins.input", return_value="n")
    def test_main_scenario_user_aborts(self, mock_input, mock_get, mock_pyproject_path, monkeypatch, capsys):
        """
        Integration test for user aborting the process.
        """
        mock_pyproject_path.write_text("[project]\nname = 'my-package'\nversion = '1.0.0'")
        mock_get.return_value.status_code = 404
        monkeypatch.setattr(sys, "argv", ["release.py", "patch"])

        r.main()

        updated_config = toml.load(mock_pyproject_path)
        assert updated_config["project"]["version"] == "1.0.0"
        
        captured = capsys.readouterr()
        assert "Aborted by user" in captured.out
