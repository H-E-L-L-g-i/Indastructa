> The English version is provided after the Ukrainian version.


# Посібник з робочих процесів (Workflows)

Цей документ пояснює мету та функціонування робочих процесів CI/CD у цьому проєкті.

## 1. `ci.yml` - Безперервна інтеграція (Continuous Integration)

Це основний робочий процес для забезпечення якості коду.

- **Тригер:** Запускається на кожен `push` та `pull_request` до гілок `main` та `dev`.
- **Мета:** Раннє виявлення помилок та проблем зі стилем коду.
- **Завдання (Jobs):**
    1.  **`lint`**: Запускає `pre-commit` для перевірки форматування коду, проблем зі стилем та базових синтаксичних помилок. Це гарантує, що весь код відповідає стандартам проєкту.
    2.  **`test`**: Запускає повний набір тестів `pytest` на кількох версіях Python (3.10, 3.11, 3.12, 3.13). Він також генерує звіт про покриття коду тестами та завантажує його на Codecov. Це гарантує, що нові зміни не ламають наявну функціональність.

Цей робочий процес **не публікує** жодних пакетів. Його єдине завдання — перевірка якості коду.

## 2. `build-and-publish.yml` - Збірка та публікація

Цей робочий процес відповідає за всі публікації пакета. Він дотримується безпечної моделі "Staging -> Production".

- **Тригери:**
    1.  **Ручний (`workflow_dispatch`):** Може бути запущений вручну із вкладки "Actions" на GitHub. Це корисно для створення тестових релізів з будь-якої гілки.
    2.  **Тег (`push: tags: 'v*.*.*'`):** Автоматично запускається, коли новий тег версії (наприклад, `v0.2.0`) надсилається до репозиторію. Це є тригером для офіційного релізу.

- **Завдання (Jobs):**
    1.  **`build`**:
        - Підвищує версію, якщо спрацював ручний тригер.
        - Збирає пакет Python (`.whl` та `.tar.gz`).
        - Завантажує зібраний пакет як артефакт з назвою `dist`. Це гарантує, що той самий пакет буде використовуватися на всіх наступних етапах.

    2.  **`publish-to-testpypi`**:
        - Завантажує артефакт `dist`.
        - Публікує пакет на **TestPyPI**. Це слугує "проміжним" середовищем (staging). Кожен офіційний реліз автоматично публікується спочатку тут.

    3.  **`publish-to-pypi`**:
        - **Залежить від `publish-to-testpypi`**.
        - **Запускається лише для офіційних тегів версій (`v*.*.*`)**.
        - **Потребує ручного схвалення**: Це завдання використовує GitHub Environment з назвою `pypi`, яке налаштоване на призупинення робочого процесу в очікуванні схвалення деплою від супроводжувача.
        - Після схвалення воно завантажує **той самий артефакт `dist`** і публікує його в основному репозиторії **PyPI**.

Така конфігурація забезпечує надійний, безпечний та гнучкий процес релізу, поєднуючи повну автоматизацію з критично важливим ручним контролем.

---

# Guide to Project Workflows

This document explains the purpose and function of the CI/CD workflows in this project.

## 1. `ci.yml` - Continuous Integration

This is the primary workflow for ensuring code quality.

- **Trigger:** Runs on every `push` and `pull_request` to the `main` and `dev` branches.
- **Purpose:** To catch errors and style issues early.
- **Jobs:**
    1.  **`lint`**: Runs `pre-commit` to check for code formatting, style issues, and basic syntax errors. This ensures all code adheres to the project's standards.
    2.  **`test`**: Runs the full `pytest` suite across multiple Python versions (3.10, 3.11, 3.12, 3.13). It also generates a code coverage report and uploads it to Codecov. This guarantees that new changes don't break existing functionality.

This workflow **does not** publish any packages. Its only job is to validate code quality.

## 2. `build-and-publish.yml` - Build and Publish

This workflow is responsible for all package publications. It follows a safe "Staging -> Production" model.

- **Triggers:**
    1.  **Manual (`workflow_dispatch`):** Can be run manually from the GitHub Actions tab. This is useful for creating test releases from any branch.
    2.  **Tag (`push: tags: 'v*.*.*'`):** Automatically runs when a new version tag (e.g., `v0.2.0`) is pushed to the repository. This is the trigger for an official release.

- **Jobs:**
    1.  **`build`**:
        - Bumps the version if triggered manually.
        - Builds the Python package (`.whl` and `.tar.gz`).
        - Uploads the built package as an artifact named `dist`. This ensures the same package is used in all subsequent steps.

    2.  **`publish-to-testpypi`**:
        - Downloads the `dist` artifact.
        - Publishes the package to **TestPyPI**. This serves as a "staging" environment. Every official release is automatically published here first.

    3.  **`publish-to-pypi`**:
        - **Depends on `publish-to-testpypi`**.
        - **Runs only for official version tags (`v*.*.*`)**.
        - **Requires manual approval**: This job uses a GitHub Environment named `pypi` which is configured to pause the workflow and wait for a maintainer to approve the deployment.
        - After approval, it downloads the **same `dist` artifact** and publishes it to the main **PyPI** repository.

This setup provides a robust, secure, and flexible release process, combining full automation with critical manual oversight.

---

##
