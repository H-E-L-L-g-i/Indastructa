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

**Indastructa** — це зручний CLI-інструмент для швидкого створення наочного ASCII-дерева файлової структури вашого проєкту.

Ідеально підходить для документації, технічних рев'ю, обговорення архітектури або публікацій у блогах.

---

## Ключові можливості

* **Нуль залежностей:** `indastructa` створено з використанням лише стандартної бібліотеки Python. Жодних зовнішніх пакетів, що гарантує швидке, безпечне та безконфліктне встановлення.
* **Наочний вивід:** Генерує красиве та зрозуміле ASCII-дерево.
* **Автоматичне збереження:** Результат автоматично зберігається у файл `project_structure.txt` в корені проєкту.
* **Розумні винятки:** За замовчуванням ігнорує непотрібні файли та папки (такі як `.git`, `venv`, `__pycache__`, `.idea` та інші).
* **Інтеграція з `.gitignore`:** Автоматично зчитує правила з `.gitignore` та `.dockerignore`, щоб виключити все, що не стосується вихідного коду.
* **Гнучке налаштування:** Дозволяє задавати цільову папку, обмежувати глибину сканування, а також додавати власні винятки та включення через аргументи командного рядка.

---

## Встановлення
```bash
pip install indastructa
```

> <details>
> <summary><u>Розширено: Встановлення з TestPyPI</u> (натисніть, щоб розкрити)</summary>
> 
> TestPyPI — це наше тестове середовище для перевірки релізів перед публікацією на PyPI.
> 
> Версії тут можуть бути новішими, старішими або збігатися з основною версією — використовуйте лише для тестування.
> 
> Щоб встановити з TestPyPI:
> ```bash
> pip install -i https://test.pypi.org/simple/ indastructa
> ```
> 
> Останні тестові версії: https://test.pypi.org/project/indastructa/
>
> </details>

---

## Використання

### Базові приклади

**Сканувати поточну директорію:**
```bash
indastructa
```

**Сканувати конкретну директорію:**
```bash
indastructa ./src
```

**Вказати файл для запису:**
```bash
indastructa -o structure.txt
```

### Розширені опції

**"Тихий" режим (без виводу в консоль):**
```bash
indastructa --quiet
```

**Попередній перегляд без збереження:**
```bash
indastructa --dry-run
```

**Обмежити глибину сканування:**
```bash
indastructa --depth 2
```

**Виключити один шаблон:**
```bash
indastructa --exclude "*.pyc"
```

**Виключити кілька шаблонів:**
```bash
indastructa --exclude "*.log,node_modules"
```

**Примусово включити один файл (має пріоритет над виключенням):**
```bash
indastructa --include ".env"
```

**Примусово включити кілька файлів:**
```bash
indastructa --include ".env,.secrets"
```

### Комбінований приклад
```bash
indastructa ./src --depth 3 --exclude "*.pyc,__pycache__" --include ".env" --quiet -o structure.md
```

### Поради

*   Використовуйте лапки для шаблонів із символами узагальнення: `"*.log"`
*   Розділяйте кілька шаблонів комою: `"*.pyc,*.pyo"`
*   Файли, що відповідають `--include`, будуть показані, навіть якщо вони відповідають `--exclude`
*   Файл для виводу за замовчуванням: `project_structure.txt`
*   Глибина сканування за замовчуванням: необмежена (-1)

---

## Логіка винятків

`indastructa` використовує систему фільтрації з таким пріоритетом:

1. **Правила `--include`:** Найвищий пріоритет. Файли, що відповідають шаблону, завжди будуть показані.
2. **Вбудовані правила:** Стандартний набір винятків, як-от `.git`, `venv`, `__pycache__` тощо.
3. **`.gitignore` та `.dockerignore`:** Автоматично завантажуються з вашого проєкту.
4. **Правила `--exclude`:** Додаткові шаблони, передані через командний рядок.

---

## Ідеї на майбутнє

Заплановані функції для майбутніх випусків:

- Вибір файлів ігнорування
- Інтерактивний режим для покрокового налаштування
- Експорт у формати JSON/YAML
- Кольоровий вивід
- Інтеграція з генераторами документації

Маєте ідеї чи знайшли помилку? [Створіть Issue](https://github.com/H-E-L-L-g-i/Indastructa/issues) на GitHub.

---

## Ліцензія

Цей проєкт розповсюджується за ліцензією MIT.
