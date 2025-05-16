# PartielsPy
A Python Wrapper for Partiels
# PartielsPy
<p>
    <a href="https://github.com/Ircam-Partiels/PartielsPy/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

A Python Wrapper for **[Partiels](https://github.com/Ircam-Partiels/Partiels)**


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
flake8 src tests
```
