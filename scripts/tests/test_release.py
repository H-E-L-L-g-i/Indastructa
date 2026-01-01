import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path
import toml
import subprocess

# Add the parent directory to the path so we can import the release script
sys.path.append(str(Path(__file__).parent.parent))

# Import the script to be tested
import release as r


@pytest.fixture
def mock_pyproject(tmp_path):
    """Creates a mock pyproject.toml file and patches the script's path."""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[project]\nname = "my-package"\nversion = "1.2.3"')
    with patch("release.PYPROJECT_PATH", pyproject_path):
        yield pyproject_path


@pytest.fixture
def mock_git_clean(monkeypatch):
    """Mocks git commands to simulate a clean repository on the main branch."""
    mock_run = MagicMock()
    # Provide enough mock results for a full successful run
    mock_run.side_effect = [
        MagicMock(stdout=""),  # 1. git status --porcelain (clean)
        MagicMock(stdout="main"),  # 2. git rev-parse (on main branch)
        MagicMock(),  # 3. git add
        MagicMock(),  # 4. git commit
        MagicMock(stdout=""),  # 5. git tag (list) -> returns no existing tags
        MagicMock(),  # 6. git tag (create)
    ]
    monkeypatch.setattr("release.subprocess.run", mock_run)
    return mock_run


# --- Unit Tests for Helper Functions ---


def test_bump_version_string():
    """Tests the version bumping logic."""
    assert r.bump_version_string("1.2.3", "patch") == "1.2.4"
    assert r.bump_version_string("1.2.3", "minor") == "1.3.0"
    assert r.bump_version_string("1.2.3", "major") == "2.0.0"
    assert r.bump_version_string("1.9.10", "minor") == "1.10.0"


def test_bump_version_string_invalid_part():
    """Tests that bumping with an invalid part exits the script."""
    with pytest.raises(SystemExit):
        r.bump_version_string("1.2.3", "invalid_part")


def test_get_project_info_no_file(capsys):
    """Tests behavior when pyproject.toml is missing."""
    with patch("release.PYPROJECT_PATH", Path("non_existent_file.toml")):
        with pytest.raises(SystemExit):
            r.get_project_info()
    captured = capsys.readouterr()
    assert "Error: pyproject.toml not found" in captured.out


def test_run_command_error(capsys):
    """Tests that run_command exits and prints stderr on failure."""
    with patch(
        "release.subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "cmd", stderr="git error"),
    ):
        with pytest.raises(SystemExit):
            r.run_command(["git", "fail"], "Test failure")
    captured = capsys.readouterr()
    assert "Error: Test failure" in captured.out
    assert "Stderr: git error" in captured.out


# --- Integration-like Tests for main() ---


def test_main_successful_patch_release(mock_pyproject, mock_git_clean, monkeypatch):
    """Tests a successful patch release scenario with user confirmation."""
    monkeypatch.setattr(sys, "argv", ["release.py", "patch"])

    with patch("builtins.input", return_value="y"):
        r.main()

    assert mock_git_clean.call_count == 6
    mock_git_clean.assert_any_call(
        ["git", "add", str(mock_pyproject)], check=True, capture_output=True, text=True
    )
    mock_git_clean.assert_any_call(
        ["git", "commit", "-m", "chore: Release v1.2.4"],
        check=True,
        capture_output=True,
        text=True,
    )
    mock_git_clean.assert_any_call(
        ["git", "tag", "v1.2.4"], check=True, capture_output=True, text=True
    )

    config = toml.load(mock_pyproject)
    assert config["project"]["version"] == "1.2.4"


def test_main_aborted_by_user(mock_pyproject, monkeypatch, capsys):
    """Tests that the script aborts if the user does not confirm."""
    mock_run = MagicMock()
    mock_run.side_effect = [MagicMock(stdout=""), MagicMock(stdout="main")]
    monkeypatch.setattr("release.subprocess.run", mock_run)
    monkeypatch.setattr(sys, "argv", ["release.py", "minor"])

    with patch("builtins.input", return_value="n"):
        with pytest.raises(SystemExit):
            r.main()

    assert mock_run.call_count == 2
    config = toml.load(mock_pyproject)
    assert config["project"]["version"] == "1.2.3"
    assert "Aborted." in capsys.readouterr().out


def test_main_with_yes_flag(mock_pyproject, mock_git_clean, monkeypatch):
    """Tests that the --yes flag skips confirmation."""
    monkeypatch.setattr(sys, "argv", ["release.py", "major", "--yes"])

    r.main()

    assert mock_git_clean.call_count == 6
    mock_git_clean.assert_any_call(
        ["git", "commit", "-m", "chore: Release v2.0.0"],
        check=True,
        capture_output=True,
        text=True,
    )
    mock_git_clean.assert_any_call(
        ["git", "tag", "v2.0.0"], check=True, capture_output=True, text=True
    )

    config = toml.load(mock_pyproject)
    assert config["project"]["version"] == "2.0.0"


def test_main_dirty_working_directory(mock_pyproject, monkeypatch, capsys):
    """Tests that the script exits if the git working directory is not clean."""
    mock_run = MagicMock(stdout=" M some_file.py")
    monkeypatch.setattr("release.subprocess.run", mock_run)
    monkeypatch.setattr(sys, "argv", ["release.py", "patch"])

    with pytest.raises(SystemExit):
        r.main()

    captured = capsys.readouterr()
    assert "Error: Your working directory is not clean." in captured.out
    mock_run.assert_called_with(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )


def test_main_wrong_branch_and_abort(mock_pyproject, monkeypatch, capsys):
    """Tests the warning on a wrong branch and user abort."""
    mock_run = MagicMock()
    mock_run.side_effect = [
        MagicMock(stdout=""),
        MagicMock(stdout="feature-branch"),
    ]
    monkeypatch.setattr("release.subprocess.run", mock_run)
    monkeypatch.setattr(sys, "argv", ["release.py", "patch"])

    with patch("builtins.input", return_value="n"):
        with pytest.raises(SystemExit):
            r.main()

    captured = capsys.readouterr()
    assert "Warning: You are on branch 'feature-branch', not 'main'." in captured.out
    assert "Aborted." in captured.out


def test_main_wrong_branch_and_proceed(mock_pyproject, monkeypatch):
    """Tests proceeding on a wrong branch after confirmation."""
    mock_run = MagicMock()
    mock_run.side_effect = [
        MagicMock(stdout=""),
        MagicMock(stdout="feature-branch"),
        MagicMock(),
        MagicMock(),
        MagicMock(stdout=""),
        MagicMock(),
    ]
    monkeypatch.setattr("release.subprocess.run", mock_run)
    monkeypatch.setattr(sys, "argv", ["release.py", "patch"])

    with patch("builtins.input", side_effect=["y", "y"]):
        r.main()

    config = toml.load(mock_pyproject)
    assert config["project"]["version"] == "1.2.4"


def test_main_tag_already_exists(mock_pyproject, monkeypatch, capsys):
    """Tests that the script warns but continues if the tag already exists."""
    mock_run = MagicMock()
    mock_run.side_effect = [
        MagicMock(stdout=""),
        MagicMock(stdout="main"),
        MagicMock(),
        MagicMock(),
        MagicMock(stdout="v1.2.4\nv1.2.3"),  # git tag list contains the new tag
    ]
    monkeypatch.setattr("release.subprocess.run", mock_run)
    monkeypatch.setattr(sys, "argv", ["release.py", "patch", "--yes"])

    r.main()

    captured = capsys.readouterr()
    assert "Warning: Tag v1.2.4 already exists. Skipping tag creation." in captured.out
    # Check that 'git tag' was not called for creation
    # 1. status, 2. branch, 3. add, 4. commit, 5. tag list
    assert mock_run.call_count == 5
