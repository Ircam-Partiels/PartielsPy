# PartielsPy
A Python Wrapper for **[Partiels](https://github.com/Ircam-Partiels/Partiels)**

## Prerequisites

This package requires **Python 3.11 or later**.

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

## Generate the Documentation
```sh
cd PartielsPy
```
- Linux, MacOS
```
.venv/bin/python3 -m pip install sphinx
sphinx-apidoc -o ./docs ./src/PartielsPy ./src/PartielsPy/templates/*
sphinx-build -b html ./docs ./docs/_build/html
```
- Windows
```
.venv\Scripts\python.exe -m pip install sphinx
sphinx-apidoc -o ./docs ./src/PartielsPy --force --no-toc --exclude-pattern=**/templates/**
sphinx-build -b html ./docs ./docs/_build/html
```

The documentation files will be generated in PartielsPy/docs/_build

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

## Example

```python
from PartielsPy import Partiels, ExportConfigImage

partiels = Partiels()
audiofile = "path/to/audiofile"
output = "path/to/output/folder"
template = "path/to/template"

config = ExportConfigImage()
partiels.export(audiofile, template, output, config)

config.adapt_to_sample_rate = True
config.format = ExportConfigImage.Formats.PNG
config.width = 600
config.height = 600
config.group_overlay = True
partiels.export(audiofile, template, output, config)

config = ExportConfigImage(format=ExportConfigImage.Formats.PNG, width=200, height=200)
partiels.export(audiofile, template, output, config)
```
