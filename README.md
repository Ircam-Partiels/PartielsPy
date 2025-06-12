# PartielsPy

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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

Partiels and its plugin suite can be downloaded from the **[Partiels release page](https://github.com/Ircam-Partiels/Partiels/releases)**
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
pip install dist/partielspy-0.1.0-py3-none-any.whl
```

**Windows**
```sh
py -m venv .venv
.venv\Scripts\activate  # Activate the virtual environment
pip install build
python -m build
pip install dist\partielspy-0.1.0-py3-none-any.whl
```

## Documentation

The documentation is built using Sphinx. After running the commands below, generated HTML documentation will be available in `PartielsPy/docs/_build/html/` directory. You can view it by opening the `index.html` file in your web browser.

**Linux and MacOS**
```sh
cd PartielsPy
source .venv/bin/activate  # Activate the virtual environment
pip install sphinx
sphinx-apidoc -o ./docs ./src/partielspy ./src/partielspy/templates/* --private --separate --force --no-toc
sphinx-build -b html ./docs ./docs/_build/html
```

**Windows**
```sh
cd PartielsPy
.venv\Scripts\activate  # Activate the virtual environment
pip install sphinx
sphinx-apidoc -o ./docs ./src/partielspy --exclude-pattern=**/templates/** --private --separate --force --no-toc
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

### Basic Setup

```python
from partielspy import Partiels

# Initialize the Partiels wrapper
partiels = Partiels()

# Define paths for your files
audio_file = "path/to/audiofile.wav"
template_file = "path/to/template.ptldoc"
output_folder = "path/to/output"
```

### Catching Export Errors

If the export process fails, `PartielsPy` raises a `subprocess.CalledProcessError`.  
You can catch and handle this exception to inspect error details:

```python
from partielspy import ExportConfigImage

try:
    partiels.export(audio_file, template_file, output_folder, ExportConfigImage())
except subprocess.CalledProcessError as e:
    print(e.stderr)  # Prints detailed error message from the export process
```

### Image Export

Export analysis as visual representations:

```python
from partielspy import ExportConfigImage

# Simple export with default settings
config = ExportConfigImage()
partiels.export(audio_file, template_file, output_folder, config)

# Customized image export
config = ExportConfigImage(
    format=ExportConfigImage.Formats.PNG,  # Set image format (PNG, JPG, etc)
    width=800,                             # Image width in pixels
    height=600,                            # Image height in pixels
    group_overlay=True,                    # Overlay all analysis groups
    adapt_to_sample_rate=True              # Adjust analysis to sample rate
)
partiels.export(audio_file, template_file, output_folder, config)
```

### Structured Data Exports

#### CSV Export

Export analysis data in tabular format:

```python
from partielspy import ExportConfigCsv

# Export with custom CSV settings
config = ExportConfigCsv(
    include_header=True,                         # Include column headers
    columns_separator=ExportConfigCsv.Separators.COMMA,  # Use comma as separator
    ignore_matrix_tracks=True,                   # Skip matrix data
    adapt_to_sample_rate=True                    # Adjust to audio sample rate
)
partiels.export(audio_file, template_file, output_folder, config)
```

#### JSON Export

Export analysis as structured JSON data:

```python
from partielspy import ExportConfigJson

config = ExportConfigJson(
    include_plugin_description=True,  # Include details about processing plugins
    ignore_matrix_tracks=True,        # Exclude matrix track data
    adapt_to_sample_rate=True         # Adjust analysis to sample rate
)
partiels.export(audio_file, template_file, output_folder, config)
```

### Timeline Exports

#### CUE File Export

Generate CUE files for CD authoring or audio marking:

```python
from partielspy import ExportConfigCue

config = ExportConfigCue(
    ignore_matrix_tracks=True,   # Skip matrix data
    adapt_to_sample_rate=True    # Adjust to audio sample rate
)
partiels.export(audio_file, template_file, output_folder, config)
```

#### LAB File Export

Create label files compatible with various audio editors:

```python
from partielspy import ExportConfigLab

config = ExportConfigLab(adapt_to_sample_rate=True)
partiels.export(audio_file, template_file, output_folder, config)
```

#### Reaper Project Export

Generate files for direct import into Reaper DAW:

```python
from partielspy import ExportConfigReaper

config = ExportConfigReaper(
    reaper_type=ExportConfigReaper.ReaperTypes.MARKER,  # Export as Reaper markers
    adapt_to_sample_rate=True                          # Adjust to audio sample rate
)
partiels.export(audio_file, template_file, output_folder, config)
```

### Working with Multiple Export Types

You can process a single audio file with multiple export configurations:

```python
from partielspy import ExportConfigImage, ExportConfigCsv, ExportConfigJson

#export in multiple formats
partiels.export(audio_file, template_file, output_folder, ExportConfigImage())
partiels.export(audio_file, template_file, output_folder, ExportConfigCsv())
partiels.export(audio_file, template_file, output_folder, ExportConfigJson())
```

### Working with Multiple Audio Files and Templates

You can process multiple audio files or templates with a single export configurations:

```python
from partielspy import ExportConfigImage

config = ExportConfigImage()
# export mutiple audio files and templates with a single export format
partiels.export(audio_file_1, template_file_1, output_folder, config)
partiels.export(audio_file_2, template_file_1, output_folder, config)
partiels.export(audio_file_3, template_file_2, output_folder, config)
```