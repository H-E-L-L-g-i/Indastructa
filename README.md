# Indastructa

[![PyPI version](https://badge.fury.io/py/indastructa.svg)](https://badge.fury.io/py/indastructa)
[![Python Versions](https://img.shields.io/pypi/pyversions/indastructa.svg)](https://pypi.org/project/indastructa/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/H-E-L-L-g-i/Indastructa/actions/workflows/ci.yml/badge.svg)](https://github.com/H-E-L-L-g-i/Indastructa/actions)
[![codecov](https://codecov.io/gh/H-E-L-L-g-i/Indastructa/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/H-E-L-L-g-i/Indastructa/tree/main)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Indastructa** is a convenient CLI tool for quickly creating a clear ASCII tree of your project's file structure.

Perfect for documentation, technical reviews, architecture discussions, or blog posts.

---

## Key Features

* **Clear Output:** Generates a beautiful and easy-to-read ASCII tree.
* **Automatic Saving:** The result is automatically saved to a `project_structure.txt` file in the project root.
* **Smart Exclusions:** By default, it ignores unnecessary files and folders (such as `.git`, `venv`, `__pycache__`, `.idea`, and others).
* **Integration with `.gitignore`:** Automatically reads rules from `.gitignore` and `.dockerignore` to exclude everything unrelated to source code.
* **Flexible Configuration:** Allows specifying target folder, limiting scan depth, and adding custom exclusions and inclusions via command-line arguments.

---

## Installation

You can install `indastructa` from PyPI or TestPyPI.

**Stable Version (from PyPI)**

This is the recommended way to install the latest stable release.

```bash
pip install indastructa
```

**Development Version (from TestPyPI)**

To install the latest pre-release version from our test repository:

```bash
pip install --index-url https://test.pypi.org/simple/ indastructa
```

---

## How to Use

### Basic Usage

To scan the current directory, simply run the command:

```bash
indastructa
```

The result will be printed to the console and saved to `project_structure.txt`.

### Specifying a Path

You can scan any directory by providing a relative or absolute path:

```bash
# Scan a subdirectory
indastructa ./src

# Scan a directory using an absolute path
indastructa C:\Users\YourUser\Projects\MyProject
```

---

## Advanced Usage

You can combine flags to customize the output.

*   **Limit scan depth** with `--depth`:

    ```bash
    indastructa --depth 2
    ```

*   **Exclude files and folders** with `--exclude` (use quotes for multiple patterns):

    ```bash
    indastructa --exclude "*.md,docs,build"
    ```

*   **Force include files** with `--include` to show them even if they are in `.gitignore`:

    ```bash
    indastructa --include .env
    ```

*   **Save to a different file** with `-o` or `--output`:

    ```bash
    indastructa -o custom_structure.md
    ```

*   **Suppress console output** with `-q` or `--quiet`:

    ```bash
    indastructa --quiet
    ```

*   **Perform a dry run** with `--dry-run` to see the output without saving the file:

    ```bash
    indastructa --dry-run
    ```

---

## 📚 Examples

### Example 1: Python Package

**Command:**
```bash
indastructa --depth 3 --exclude "*.pyc,__pycache__,dist,build"
```

**Output:**
```
my_package/
  |-- src/
  |     |-- __init__.py
  |     |-- main.py
  |     +-- utils.py
  |-- tests/
  |     |-- test_main.py
  |     +-- test_utils.py
  |-- setup.py
  |-- README.md
  +-- requirements.txt
```

---

### Example 2: Web Application

**Command:**
```bash
indastructa --exclude "node_modules,dist,.next"
```

**Output:**
```
my_app/
  |-- public/
  |-- src/
  |     |-- components/
  |     |-- pages/
  |     +-- styles/
  |-- package.json
  +-- README.md
```

---

### Example 3: CI/CD Usage in GitHub Actions

Add this to your workflow to automatically add the project structure to the job summary:

```yaml
- name: Generate and display project structure
  run: |
    pip install indastructa
    indastructa --depth 3 -o structure.txt

    echo "## 📂 Project Structure" >> $GITHUB_STEP_SUMMARY
    echo '```' >> $GITHUB_STEP_SUMMARY
    cat structure.txt >> $GITHUB_STEP_SUMMARY
    echo '```' >> $GITHUB_STEP_SUMMARY
```

---

## Exclusion Logic

`indastructa` uses a filtering system with the following priority:

1. **`--include` rules:** Patterns passed via `--include` have the highest priority. If a file matches, it will always be shown.
2. **Built-in rules:** A default set of common exclusions like `.git`, `venv`, `__pycache__`, etc.
3. **Rules from `.gitignore` and `.dockerignore`:** Automatically loaded from your project.
4. **`--exclude` rules:** Patterns passed via `--exclude`.

---

## Future Ideas

For more advanced feature ideas, see the `FUTURE_FEATURES.md` file in this repository.

- Selectable ignore files
- Interactive mode
- Support for exporting to JSON/YAML

Have ideas or found a bug? Create an Issue on GitHub.

---

## License

The project is distributed under the MIT License.
