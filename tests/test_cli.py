import pytest
from pathlib import Path
import sys
from indastructa_pkg.cli import main, format_dir_structure

# Add the project root to the path to allow importing the package
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def project_structure(tmp_path: Path) -> Path:
    """
    Creates a temporary directory structure for testing.
    Returns the root path of the created structure.
    """
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    # Files and directories to be included
    (project_dir / "src").mkdir()
    (project_dir / "src" / "main.py").touch()
    (project_dir / "src" / "api").mkdir()
    (project_dir / "src" / "api" / "helpers.py").touch()
    (project_dir / "README.md").touch()

    # Files and directories to be excluded
    (project_dir / ".git").mkdir()
    (project_dir / "venv").mkdir()
    (project_dir / ".env").touch()

    # .gitignore file for testing its parsing
    (project_dir / ".gitignore").write_text("*.log\n__pycache__/\n")
    (project_dir / "app.log").touch()
    (project_dir / "src" / "__pycache__").mkdir()

    return project_dir


def test_format_dir_structure_output(project_structure: Path):
    """
    Tests that the format_dir_structure function correctly formats the tree,
    ignoring nothing when the exclude set is empty.
    """
    # --- FIX: Use the correct keyword argument 'exclude_patterns' ---
    result = format_dir_structure(project_structure, exclude_patterns=set())

    assert "src/" in result
    assert "main.py" in result
    assert ".git/" in result
    assert "venv/" in result


def test_main_with_exclusions(project_structure: Path, monkeypatch):
    """
    Integration test for the main function.
    Checks that default exclusions and .gitignore patterns work correctly.
    """
    output_file = project_structure / "project_structure.txt"

    # Imitate the command: 'indastructa /path/to/test_project'
    monkeypatch.setattr('sys.argv', ['indastructa', str(project_structure)])

    main()

    assert output_file.is_file()

    content = output_file.read_text(encoding="utf-8")

    assert "src/" in content
    assert "README.md" in content
    assert ".gitignore" in content

    assert ".git/" not in content
    assert "venv/" not in content
    assert ".env" not in content
    assert "app.log" not in content
    assert "__pycache__" not in content


def test_main_with_depth_limit(project_structure: Path, monkeypatch):
    """
    Tests the --depth argument.
    """
    output_file = project_structure / "project_structure.txt"
    monkeypatch.setattr('sys.argv',
                        ['indastructa', str(project_structure), "--depth", "1"])

    main()

    content = output_file.read_text(encoding="utf-8")

    assert "src/" in content
    assert "README.md" in content

    assert "main.py" not in content
    assert "api/" not in content


def test_main_with_custom_exclude(project_structure: Path, monkeypatch):
    """
    Tests the --exclude argument.
    """
    output_file = project_structure / "project_structure.txt"
    monkeypatch.setattr('sys.argv',
                        ['indastructa', str(project_structure), "--exclude", "src"])

    main()

    content = output_file.read_text(encoding="utf-8")

    assert "src" not in content
    assert "main.py" not in content
