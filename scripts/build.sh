#!/bin/bash

python -m build
python -m pip install dist/partielspy-*.whl --force-reinstall
pytest -s tests -v
