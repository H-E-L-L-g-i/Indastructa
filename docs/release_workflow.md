# "Adult" Release Workflow Idea

This document outlines a plan for a highly automated, safe, and interactive release script (`scripts/release.py`). This represents a "gold standard" for release automation.

## Core Philosophy

The release script should act as a smart **orchestrator** and **gatekeeper**. It should handle all the repetitive tasks but leave the final, irreversible action (the `push`) to the developer.

## Key Stages of the "Adult" Script

### 1. Pre-flight Checks (Safety First)

Before making any changes, the script must verify that the environment is ready for a release.

- [ ] **Clean Git Working Directory**: Check `git status --porcelain`. If there are uncommitted changes, abort with a clear error message.
- [ ] **Correct Branch**: Ensure the release is being run from a designated release branch (e.g., `main` or `dev`). If not, warn the user and ask for confirmation.
- [ ] **Sync with Remote**: Run `git fetch` and check if the local branch is behind the remote counterpart (`git status -uno`). If it is, abort and instruct the user to `git pull`.
- [ ] **Tests Pass**: Automatically run `pytest`. If any tests fail, abort.
- [ ] **CHANGELOG Check**: Check if `CHANGELOG.md` has been updated for the new version (this is an advanced check, can be added later).

### 2. Interactive Planning & Confirmation

The script should clearly communicate its intentions.

- [ ] **Calculate New Version**: Determine the new version string based on the `major`, `minor`, or `patch` argument.
- [ ] **Display Plan**: Show the user a summary of the actions it will perform:
  ```
  I will perform the following actions:
    - Bump version from 0.1.0 to 0.2.0 in pyproject.toml
    - Update CHANGELOG.md to move [Unreleased] changes to [0.2.0]
    - Create commit: "chore: Release v0.2.0"
    - Create tag: "v0.2.0"
  ```
- [ ] **Single Confirmation**: Ask a single, final question: `Proceed with release? (y/N)`. The default answer should be "No".
- [ ] **`--yes` Flag**: A `--yes` flag should bypass this confirmation for automation purposes.

### 3. Execution (The "Work")

If the user confirms, the script performs all the actions.

- [ ] **Update `pyproject.toml`**: Change the version number.
- [ ] **Update `CHANGELOG.md`**: Automatically move the content from the `[Unreleased]` section to a new `[vX.Y.Z]` section.
- [ ] **Create Git Commit**: Run `git add pyproject.toml CHANGELOG.md` and `git commit -m "chore: Release vX.Y.Z"`.
- [ ] **Create Git Tag**: Run `git tag vX.Y.Z`.

### 4. Post-flight Instructions (Final Hand-off)

After completing its work, the script gives the user the final, manual command.

- [ ] **Display Success Message**:
  ```
  Success! Release commit and tag 'v0.2.0' have been created locally.
  ```
- [ ] **Provide Final Command**:
  ```
  NEXT STEP: Push the changes to trigger the publication workflow:

      git push && git push --tags
  ```

## Example Usage

A developer would simply run:

```bash
python scripts/release.py minor
```

The script would then guide them through all the checks and actions, leaving only the final `push` to them. This combines safety, automation, and human oversight in a very robust way.
