# PartielsPy

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Ircam-Partiels/PartielsPy/actions/workflows/ci.yml/badge.svg)](https://github.com/Ircam-Partiels/PartielsPy/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/Documentation-green.svg)](https://ircam-partiels.github.io/PartielsPy/)

A Python wrapper for **[Partiels](https://github.com/Ircam-Partiels/Partiels)** — a powerful audio analysis toolkit for spectral processing and transformation.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Documentation](#documentation)
- [Code Style](#code-style)
- [Debugging](#debugging)
- [Usage Examples](#usage-examples)

## Overview

PartielsPy provides a Python interface to the Partiels audio analysis system, allowing you to:
- Work with templates for consistent analysis configurations
- Export analysis data in various formats (images, CSV, JSON, etc.)
- Customize export configurations through a simple API

## Prerequisites

This package requires:
- **Python 3.11 or later**
- **Partiels**
- **Partiels plugin suite** 

Partiels and its plugin suite can be downloaded from the **[Partiels release page](https://github.com/Ircam-Partiels/Partiels/releases)**. You can use the [scripts/install_partiels.sh](./scripts/install_partiels.sh) (Unix) and [scripts/install_partiels.ps1](./scripts/install_partiels.ps1) (Windows) scripts to download and install automatically Partiels and its plugin suite.

## Installation

PartielsPy can be installed either directly from GitHub using pip, or from source after cloning the repository.

### Install via GitHub

**Linux and macOS:**
```sh
python3 -m venv .venv
source .venv/bin/activate  # Activate the virtual environment
pip install git+https://github.com/Ircam-Partiels/PartielsPy.git
```

**Windows:**
```sh
py -m venv .venv
.venv\Scripts\activate  # Activate the virtual environment
pip install git+https://github.com/Ircam-Partiels/PartielsPy.git
```

### Install from Source
```sh
git clone https://github.com/Ircam-Partiels/PartielsPy.git
cd PartielsPy
```

**Linux and macOS**
```sh
python3 -m venv .venv
source .venv/bin/activate  # Activate the virtual environment
pip install build
python -m build
pip install dist/partielspy-*.whl
```

**Windows**
```sh
py -m venv .venv
.venv\Scripts\activate  # Activate the virtual environment
pip install build
python -m build
pip install dist\partielspy-*.whl
```

## Documentation

The documentation is built using Sphinx. After running the commands below, generated HTML documentation will be available in `PartielsPy/docs/_build/html/` directory. You can view it by opening the `index.html` file in your web browser.

**Linux and MacOS**
```sh
cd PartielsPy
source .venv/bin/activate  # Activate the virtual environment
pip install sphinx furo
sphinx-build -b html ./docs ./docs/_build/html
```

**Windows**
```sh
cd PartielsPy
.venv\Scripts\activate  # Activate the virtual environment
pip install sphinx furo
sphinx-build -b html ./docs ./docs/_build/html
```

## Code Style

This project uses the following tools to enforce consistent code quality:

- [`black`](https://black.readthedocs.io/en/stable/): An uncompromising Python code formatter
- [`isort`](https://pycqa.github.io/isort/): Automatically sorts and organizes imports
- [`flake8`](https://flake8.pycqa.org/): Checks code style and potential errors

### Installing the tools

```sh
pip install black isort flake8
```

### Code style commands

```sh
# Check code style without making changes
black --check .
isort --check-only .
flake8 src tests examples

# Apply formatting
black .
isort .
```
## Debugging

PartielsPy includes comprehensive logging to help troubleshoot issues during development. You can configure Python's logging module to display these messages by setting the DEBUG level.

### Debug Configuration

Enable all debug messages with this simple configuration:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Levels

PartielsPy logging only uses the DEBUG level. To disable the debug messages you can set the logging level to any other level:
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

## Usage Examples

PartielsPy provides a simple, flexible API for analyzing audio files and exporting the results in various formats. Here are some examples showing how to use the library, you can find more practical examples **[here](examples)**.

### Example of document export

```python
from partielspy import Partiels, Document, ExportConfig
import subprocess

# Initialize the Partiels wrapper
partiels = Partiels()

# Load the document with a Partiels document and an audio file
document = Document(document_file="path/to/template.ptldoc", audio_file_layout="path/to/audiofile.wav")

# Configure the export in the PNG format (the export format can be CSV, LAB, CUE, REAPER, JSON, PNG or JPG)
export_config = ExportConfig(
    format=ExportConfig.Formats.PNG,    # Format
    image_width=800,                    # Image width in pixels
    image_height=600,                   # Image height in pixels
    image_ppi=144,                      # Image pixel density in pixels per inch
    image_group_overlay=True            # Overlay all analysis groups
)

# Analyze and export the results
try:
    partiels.export(document, "path/to/output", export_config)
except subprocess.CalledProcessError as e:
    print(e.stderr)  # Prints detailed error message from the export process

# Configure the export in the CSV format
export_config = ExportConfig(
    format=ExportConfig.Formats.CSV,                                # Format
    csv_include_header=True,                                        # Include CSV column headers
    csv_columns_separator=ExportConfig.CsvColumnSeparators.COMMA,   # Use comma as CSV column separators
    ignore_matrix_tracks=True                                       # Skip matrix tracks
)

# Analyze and export the results
try:
    partiels.export(document, "path/to/output", export_config)
except subprocess.CalledProcessError as e:
    print(e.stderr)  # Prints detailed error message from the export process  
```

### Example of document editing
```python
from partielspy import *

# Create a Document with an audio file
document = Document(audio_file_layout="path/to/audiofile.wav")

# Create a Group
group = Group("Group")

# Create a Track with a plugin
track_1 = Track("Track With Plugin")
track_1.plugin_key = PluginKey("plugin-identifier", "plugin-feature")

# Create a Track and with a precomputed file
track_2 = Track("Track With File")
track_2.file_info = FileInfo("path/to/import/file.csv")

# Add Tracks to the group
group.add_track(track_1)
group.add_track(track_2)

# Add Group to the Document
document.add_group(group)

# Export the Document as CSV and JPEG
partiels.export(document, "path/to/output", ExportConfig(format=ExportConfig.Formats.JSON))

# Save the Document to a ptldoc file for later
document.save("path/to/save/file.ptldoc")
```
