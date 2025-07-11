import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "../src"))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PartielsPy"
copyright = "2025 IRCAM"
author = "Pierre Guillot and Thomas Barbé"
release = "0.3.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

exclude_patterns = ["_build", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"


def skip_member(app, what, name, obj, skip, options):
    if name.startswith("_"):
        return True
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip_member)
