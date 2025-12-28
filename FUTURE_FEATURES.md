# Future Feature Ideas for Indastructa

This document contains ideas for new features that could be implemented in the future to make the tool even more powerful and flexible.

---

## High Priority (Before v1.0.0)

- [ ] **Add `--yes` flag to `scripts/release.py`**: To skip confirmation prompts, which is essential for automation and CI/CD scripts.
- [ ] **Create `CONTRIBUTING.md`**: To lower the barrier for new contributors by providing clear guidelines for setup, testing, and pull requests.
- [ ] **Add Badges to `README.md`**: To give the project a professional look and provide at-a-glance information about its status (PyPI version, tests, coverage, etc.).

## Medium Priority (After v1.0.0)

- [ ] **Implement Git Status Check in `scripts/release.py`**: To prevent releases from a "dirty" working directory, ensuring that the release tag corresponds to a clean, committed state.
- [ ] **Add `--quiet` / `-q` flag to `indastructa`**: To suppress console output and only save the structure to a file, making the tool more "unix-friendly" and usable in pipelines.
- [ ] **Add More Examples to READMEs**: Enhance both `README.md` and `README_ua.md` with more real-world examples of using the CLI tool.

## Low Priority (Future Enhancements)

- [ ] **Implement Logging in `scripts/release.py`**: To keep a history of all release operations for auditing and debugging purposes.
- [ ] **Create a Dedicated `docs/` Folder**: For more extensive documentation, including detailed guides, API references, and advanced examples, as the project grows.
- [ ] **Add Selectable Ignore File**: Allow users to specify a custom ignore file (`--ignore-file`) or disable default ignores (`--no-default-ignores`, `--no-gitignore`).
- [ ] **Implement Interactive Mode (`-i`)**: Guide the user through the process of generating a structure with interactive prompts for path, exclusions, depth, etc.

---

*This plan was formulated based on the expert suggestions provided on 2024-05-15.*
