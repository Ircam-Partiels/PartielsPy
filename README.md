# PartielsPy
A Python Wrapper for Partiels
# PartielsPy
<p>
    <a href="https://github.com/Ircam-Partiels/PartielsPy/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

A Python Wrapper for **[Partiels](https://github.com/Ircam-Partiels/Partiels)**

## Compilation

```sh
git clone git@github.com:Ircam-Partiels/PartielsPy.git
cd PartielsPy

# Linux, MacOS
python3 -m venv .venv
.venv/bin/python3 -m pip install build
.venv/bin/python3 -m build
.venv/bin/python3 -m pip install dist/partielspy-0.0.0-py3-none-any.whl

# Windows
py -m venv .venv
.venv\Scripts\python.exe -m pip install build
.venv\Scripts\python.exe -m build
.venv\Scripts\python.exe -m pip install dist\partielspy-0.0.0-py3-none-any.whl
```

## Code Style

This project uses the following tools to enforce consistent code quality:

- [`black`](https://black.readthedocs.io/en/stable/): an uncompromising Python code formatter.
- [`isort`](https://pycqa.github.io/isort/): automatically sorts and organizes imports.
- [`flake8`](https://flake8.pycqa.org/): checks code style and potential errors.

### Custom Rules

- Maximum line length: **100 characters**

### Run Checks Locally

```bash
# Check code style without making changes
black --check .
isort --check-only .
flake8 .
