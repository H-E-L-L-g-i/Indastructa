# Indastructa

[![PyPI version](https://badge.fury.io/py/indastructa.svg)](https://badge.fury.io/py/indastructa)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/indastructa?period=total&units=international_system&left_color=gray&right_color=orange&left_text=downloads)](https://pepy.tech/projects/indastructa)
[![Python Versions](https://img.shields.io/pypi/pyversions/indastructa.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Tests](https://github.com/H-E-L-L-g-i/Indastructa/actions/workflows/ci.yml/badge.svg)](https://github.com/H-E-L-L-g-i/Indastructa/actions)
[![codecov](https://codecov.io/gh/H-E-L-L-g-i/Indastructa/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/H-E-L-L-g-i/Indastructa)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000?style=flat)](https://github.com/psf/black)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230?style=flat)](https://github.com/astral-sh/ruff)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](https://github.com/H-E-L-L-g-i/Indastructa/blob/main/pyproject.toml)

**Indastructa** is a convenient CLI tool for quickly creating a clear ASCII tree of your project's file structure.

Perfect for documentation, technical reviews, architecture discussions, or blog posts.

---

## Key Features

* **Zero Dependencies:** Built using only Python's standard library. No external packages are needed, ensuring a fast, secure, and conflict-free installation.
* **Clear Output:** Generates a beautiful and easy-to-read ASCII tree.
* **Automatic Saving:** Results are automatically saved to a `project_structure.txt` file in the project root.
* **Smart Exclusions:** By default, ignores unnecessary files and folders (such as `.git`, `venv`, `__pycache__`, `.idea`, and others).
* **Integration with `.gitignore`:** Automatically reads rules from `.gitignore` and `.dockerignore` to exclude everything unrelated to source code.
* **Flexible Configuration:** Allows specifying target folder, limiting scan depth, and adding custom exclusions and inclusions via command-line arguments.

---

## Installation
```bash
pip install indastructa
```

> <details>
> <summary><b>Advanced: Installing from TestPyPI</b></summary>
>
> TestPyPI is our testing environment for validating releases before publishing to PyPI.
>
>  Versions there may be newer, older, or match the production release - use for testing purposes only.
>
> To install from TestPyPI:
> ```bash
> pip install -i https://test.pypi.org/simple/ indastructa
> ```
>
> Latest test version: https://test.pypi.org/project/indastructa/
>
> </details>

---

## Usage

### Basic Examples

**Scan current directory:**
```bash
indastructa
```

**Scan specific directory:**
```bash
indastructa ./src
```

**Custom output file:**
```bash
indastructa -o structure.txt
```

### Advanced Options

**Quiet mode (no console output):**
```bash
indastructa --quiet
```

**Preview without saving:**
```bash
indastructa --dry-run
```

**Limit scan depth:**
```bash
indastructa --depth 2
```

**Exclude single pattern:**
```bash
indastructa --exclude "*.pyc"
```

**Exclude multiple patterns:**
```bash
indastructa --exclude "*.log,node_modules"
```

**Force include single file (overrides exclude):**
```bash
indastructa --include ".env"
```

**Force include multiple files:**
```bash
indastructa --include ".env,.secrets"
```

### Combined Example
```bash
indastructa ./src --depth 3 --exclude "*.pyc,__pycache__" --include ".env" --quiet -o structure.md
```

### Tips

*   Use quotes around patterns with wildcards: `"*.log"`
*   Separate multiple patterns with commas: `"*.pyc,*.pyo"`
*   Files matching `--include` are shown even if they match `--exclude`
*   Default output: `project_structure.txt`
*   Default depth: unlimited (-1)

---

## Exclusion Logic

`indastructa` uses a filtering system with the following priority:

1. **`--include` rules:** Highest priority. Matching files are always shown.
2. **Built-in rules:** Default exclusions like `.git`, `venv`, `__pycache__`, etc.
3. **`.gitignore` and `.dockerignore`:** Automatically loaded from your project.
4. **`--exclude` rules:** Additional patterns passed via command line.

---

## Future Ideas

Planned features for upcoming releases:

- Selectable ignore files
- Interactive mode for step-by-step configuration
- Export to JSON/YAML formats
- Color-coded output
- Integration with project documentation generators

Have ideas or found a bug? [Create an Issue](https://github.com/H-E-L-L-g-i/Indastructa/issues) on GitHub.

---

## License

This project is distributed under the MIT License.
