import subprocess
import sys
from pathlib import Path

folder = Path(__file__).parent.parent / "examples"


def test_examples():
    files = folder.glob("*.py")

    for file in files:
        try:
            result = subprocess.run(
                [sys.executable, file], capture_output=True, text=True, timeout=5
            )
        except subprocess.TimeoutExpired:
            if file.name == "export_image_and_display.py":
                continue
        if result.stderr:
            print("Errors:\n", result.stderr)
        assert result.returncode == 0, f"example {file} failed"
