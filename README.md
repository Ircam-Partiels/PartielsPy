# PartielsPy
A Python Wrapper for **[Partiels](https://github.com/Ircam-Partiels/Partiels)**

## Compilation
```sh
git clone https://github.com/Ircam-Partiels/PartielsPy.git
cd PartielsPy
```
- Linux and MacOS
```sh
python3 -m venv .venv
.venv/bin/python3 -m pip install build
.venv/bin/python3 -m build
.venv/bin/python3 -m pip install dist/partielspy-0.0.0-py3-none-any.whl
```
- Windows
```sh
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

You can run the checks locally using :
```bash
# Check code style without making changes
black --check .
isort --check-only .
flake8 src tests
```
