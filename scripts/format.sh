#!/bin/bash

black .
isort .
flake8 src tests examples
