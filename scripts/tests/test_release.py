import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path
import toml

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
        MagicMock(),  # 5. git tag
    ]
    monkeypatch.setattr("release.subprocess.run", mock_run)
    return mock_run


def test_bump_version_string():
    """Tests the version bumping logic."""
    assert r.bump_version_string("1.2.3", "patch") == "1.2.4"
    assert r.bump_version_string("1.2.3", "minor") == "1.3.0"
    assert r.bump_version_string("1.2.3", "major") == "2.0.0"
    assert r.bump_version_string("1.9.10", "minor") == "1.10.0"


def test_main_successful_patch_release(mock_pyproject, mock_git_clean, monkeypatch):
    """Tests a successful patch release scenario with user confirmation."""
    monkeypatch.setattr(sys, "argv", ["release.py", "patch"])

    # Mock user input to confirm
    with patch("builtins.input", return_value="y"):
        r.main()

    # Check that all 5 git commands were called
    assert mock_git_clean.call_count == 5
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

    # Check that the version was updated
    config = toml.load(mock_pyproject)
    assert config["project"]["version"] == "1.2.4"


def test_main_aborted_by_user(mock_pyproject, monkeypatch, capsys):
    """Tests that the script aborts if the user does not confirm."""
    # We only need to mock the first two git calls for this scenario
    mock_run = MagicMock()
    mock_run.side_effect = [
        MagicMock(stdout=""),
        MagicMock(stdout="main"),
    ]
    monkeypatch.setattr("release.subprocess.run", mock_run)
    monkeypatch.setattr(sys, "argv", ["release.py", "minor"])

    with patch("builtins.input", return_value="n"):
        with pytest.raises(SystemExit):
            r.main()

    # Only git status and branch checks should have been called
    assert mock_run.call_count == 2

    # Version should NOT be updated
    config = toml.load(mock_pyproject)
    assert config["project"]["version"] == "1.2.3"

    captured = capsys.readouterr()
    assert "Aborted." in captured.out


def test_main_with_yes_flag(mock_pyproject, mock_git_clean, monkeypatch):
    """Tests that the --yes flag skips confirmation."""
    monkeypatch.setattr(sys, "argv", ["release.py", "major", "--yes"])

    # No input should be requested, so no need to mock it.
    r.main()

    # Check that all 5 git commands were called
    assert mock_git_clean.call_count == 5
    mock_git_clean.assert_any_call(
        ["git", "commit", "-m", "chore: Release v2.0.0"],
        check=True,
        capture_output=True,
        text=True,
    )
    mock_git_clean.assert_any_call(
        ["git", "tag", "v2.0.0"], check=True, capture_output=True, text=True
    )

    # Check that the version was updated
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
    # Check that it shows the status
    mock_run.assert_called_with(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )


def test_main_wrong_branch_and_abort(mock_pyproject, monkeypatch, capsys):
    """Tests the warning on a wrong branch and user abort."""
    mock_run = MagicMock()
    mock_run.side_effect = [
        MagicMock(stdout=""),  # git status is clean
        MagicMock(stdout="feature-branch"),  # git branch is not main
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
        MagicMock(stdout=""),  # 1. git status is clean
        MagicMock(stdout="feature-branch"),  # 2. git branch is not main
        MagicMock(),  # 3. git add
        MagicMock(),  # 4. git commit
        MagicMock(),  # 5. git tag
    ]
    monkeypatch.setattr("release.subprocess.run", mock_run)
    monkeypatch.setattr(sys, "argv", ["release.py", "patch"])

    # First input for branch warning, second for release confirmation
    with patch("builtins.input", side_effect=["y", "y"]):
        r.main()

    # Check that version was updated
    config = toml.load(mock_pyproject)
    assert config["project"]["version"] == "1.2.4"
