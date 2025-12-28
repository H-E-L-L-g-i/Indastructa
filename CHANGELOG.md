# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [0.1.0] - 2024-05-16

### Added
- `--include` flag to force include files that would normally be excluded.
- `--dry-run` flag to preview output without writing to a file.
- Comprehensive tests for all CLI flags, including edge cases for `--output` and multiple `--exclude` flags.
- Unit and integration tests for `scripts/release.py` helper functions and main scenarios.
- `FUTURE_FEATURES.md` to document upcoming ideas.

### Fixed
- **CRITICAL**: `scripts/release.py` no longer incorrectly bumps the patch version when using the `--dev` flag.
- `indastructa_pkg/cli.py` now correctly handles multiple `--exclude` flags.
- `indastructa_pkg/cli.py` now correctly handles being called without arguments.
- `indastructa_pkg/cli.py` now gracefully handles `PermissionError` when scanning directories or writing files.
- Removed `assert True` from `test_publication_to_pipy.py`.
- Corrected `E402` import order error in `tests/test_cli.py`.
- Corrected type hints in `scripts/release.py` to satisfy static analysis tools.

### Changed
- Refactored `scripts/release.py`'s `main` function into smaller, more manageable helpers (`handle_bump_scenario` and `handle_check_scenario`) to reduce cognitive complexity.
- Improved test coverage from ~60% to ~90%.
- Updated `README.md` and `README_ua.md` with new examples and flags.
- Configured `pytest` to use a local temporary directory (`.pytest_tmp`) via IDE settings, and cleaned up `pytest.ini`.
- Refined the `help` messages in both CLI scripts to be more user-friendly and provide better examples.

## [0.0.16] - 2024-05-15

### Added
- Initial public release on TestPyPI.
- CLI tool for generating ASCII project structure trees.
- Support for `.gitignore` and `.dockerignore` patterns.
- Flexible exclusion options (`--exclude`).
- Depth limiting (`--depth`).
- Automatic filtering of common development artifacts.
- GitHub Actions CI/CD pipeline for automated testing and publishing.
