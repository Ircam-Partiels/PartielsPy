#!/bin/bash

rm -rf dist tests/exports examples/exports
python -m build
python -m pip install dist/partielspy-*.whl --force-reinstall
pytest -s -v tests $1
