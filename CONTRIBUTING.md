# Contributing to Indastructa

Thank you for your interest in contributing to Indastructa!

## Quick Start

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR-USERNAME/Indastructa.git
cd Indastructa
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
pip install -r requirements.txt

# Install development tools
pip install pytest pytest-cov pre-commit

# Set up pre-commit hooks
pre-commit install
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

---

## Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_cli.py -v

# Run without network tests
pytest -m "not network"
```

---

## Code Style

We use:
- **Ruff** for linting and formatting
- **Pre-commit hooks** to enforce standards
```bash
# Format code
ruff format .

# Check for issues
ruff check .

# Run pre-commit on all files
pre-commit run --all-files
```

---

## Pull Request Process

1. **Ensure tests pass:**
   ```bash
   pytest
   ```

2. **Update documentation** if needed (README.md, docstrings)

3. **Add entry to CHANGELOG.md** under `[Unreleased]`

4. **Create Pull Request** to `dev` branch

5. **Describe your changes** clearly in PR description

---

## Release Process (for maintainers)

This project uses a "Staging -> Production" release model with manual approval.

### 1. Prepare the Release
- Ensure the `dev` branch is up-to-date and all changes are merged.
- Create and merge a Pull Request from `dev` into `main`.
- Switch to the `main` branch and pull the latest changes:
  ```bash
  git checkout main
  git pull origin main
  ```

### 2. Run the Release Script
- Run the local release script to bump the version, create a commit, and tag it.
  ```bash
  # For a patch release (e.g., 0.1.0 -> 0.1.1)
  python scripts/release.py patch

  # For a minor release (e.g., 0.1.1 -> 0.2.0)
  python scripts/release.py minor
  ```

### 3. Push to Trigger Publication
- Push the newly created commit and tag to GitHub. This will trigger the `build-and-publish.yml` workflow.
  ```bash
  git push && git push --tags
  ```

### 4. Approve the Production Release
- The workflow will automatically publish the new version to **TestPyPI**.
- It will then pause before publishing to the main **PyPI**, waiting for your approval.
- Go to the "Actions" tab in the GitHub repository, find the running workflow, and click "Review deployments".
- After verifying the package on TestPyPI, click "Approve and deploy" to publish to PyPI.

---

## Reporting Bugs

Found a bug? Please create an issue with:
- **Description** of the problem
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Environment** (OS, Python version)
- **Logs** if applicable

---

## Suggesting Features

Have an idea? Open an issue with:
- **Feature description**
- **Use case** (why is it useful?)
- **Example usage** (if applicable)

---

## Documentation

- Docstrings should follow [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Update README.md for user-facing changes
- Add examples for new features

---

## Code Review Checklist

Before submitting PR, ensure:
- [ ] Tests pass (`pytest`)
- [ ] Code is formatted (`ruff format`)
- [ ] No linting errors (`ruff check`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages are clear

---

### Developer Note on Dependencies

Currently, this project has zero external dependencies. If dependencies from PyPI are added in the future, the command to install from TestPyPI should be updated to use `--extra-index-url` to ensure those dependencies are found:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ indastructa
```
