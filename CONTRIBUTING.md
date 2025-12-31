# Contributing to Indastructa

Thank you for your interest in contributing to Indastructa! 🎉

##  Quick Start

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

### Development Releases (TestPyPI)
```bash
# Push to dev branch
git push origin dev
# CI automatically publishes to TestPyPI
```

### Stable Releases (PyPI)
```bash
# Update version
python scripts/release.py major  # or minor/patch

# Push and tag
git push origin main
git push origin vX.Y.Z

# CI automatically publishes to PyPI
```

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

## Thank You!

Your contributions make Indastructa better for everyone!

Questions? Feel free to open an issue or discussion.
