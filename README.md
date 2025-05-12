# PartielsPy
<p>
    <a href="https://github.com/Ircam-Partiels/PartielsPy/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

A Python Wrapper for **[Partiels](https://github.com/Ircam-Partiels/Partiels)**

## Features

**[PartielsPy](https://github.com/Ircam-Partiels/PartielsPy)** is a python wrapper dedicated to the software **[Partiels](https://github.com/Ircam-Partiels/Partiels)** developped by [Pierre Guillot](https://github.com/pierreguillot).
This wrapper rely on the CLI of Partiels's executable, that's why to make use of this package Partiels must be beforehand installed.
The aim of this project is to allow Partiels users to script and automate the creation of backup files as well as the export of their analyses through Python.
- Windows, Mac & Linux support
- Use Partiels's export to PNG, JPEG, CSV, LAB, JSON, CUE, REAPER & SDIF formats
- Default Templates : factory, supervp and partials

## Compilation
```sh
git clone git@github.com:Ircam-Partiels/PartielsPy.git
cd PartielsPy

# Linux, MacOS
python3 -m build
python3 -m venv .venv
.venv/bin/python3 -m pip install dist/partielspy-0.0.0-py3-none-any.whl

# Windows
py -m build
py -m venv .venv
.venv\Scripts\python.exe -m pip install dist\partielspy-0.0.0-py3-none-any.whl

```
> ⚠️ Partiels must be installed to make use of PartielsPy 

## Generate the Documentation
```sh
cd PartielsPy/docs

# Linux, MacOS
make html

# Windows
make.bat
```

## Example
```py
from PartielsPy.Partiels import Partiels

partiels = Partiels()
# Create a document using factory default template
document = partiels.createDefaultDocument('/path/to/your/sample', 'factory')
jpeg_exporter = partiels.createJpegExporter()
jpeg_exporter.export(document, '/path/to/export/folder')

# Create a document using your template
document = partiels.createDocument('/path/to/your/sample', '/path/to/your/template')
csv_exporter = partiels.createCsvExporter()
csv_exporter.export(document, '/path/to/export/folder')
```

## Code Style

This project uses the following tools to enforce consistent code quality:

- [`black`](https://black.readthedocs.io/en/stable/): an uncompromising Python code formatter.
- [`isort`](https://pycqa.github.io/isort/): automatically sorts and organizes imports.
- [`flake8`](https://flake8.pycqa.org/): checks code style and potential errors.

### Custom Rules

- Maximum line length: **88 characters** (as recommended by `black`)
- Some `flake8` warnings are ignored for compatibility with `black`: `E203`, `W503`

### Run Checks Locally

```bash
# Check code style without making changes
black --check .
isort --check-only .
flake8 .
