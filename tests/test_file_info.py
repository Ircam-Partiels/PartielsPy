from pathlib import Path

import pytest

from partielspy import *

resource_dir = Path(__file__).resolve().parent.parent / "resource"


def test_file_info_creation():
    file_info = FileInfo()

    file_info = FileInfo(path=resource_dir / "marker.cue")
    assert (
        file_info.csv_columns_separator is None
    ), "The csv_columns_separator should be None"
    assert file_info.csv_use_end_time is None, "The csv_use_end_time should be None"

    file_info = FileInfo(path=resource_dir / "marker.csv")
    assert (
        file_info.csv_columns_separator == FileInfo.CsvColumnSeparators.COMMA
    ), "The csv_columns_separator should be COMMA"
    assert file_info.csv_use_end_time is False, "The csv_use_end_time should be False"

    file_info = FileInfo(
        path=resource_dir / "marker.csv",
        csv_columns_separator=FileInfo.CsvColumnSeparators.PIPE,
        csv_use_end_time=True,
    )
    assert (
        file_info.csv_columns_separator == FileInfo.CsvColumnSeparators.PIPE
    ), "The csv_columns_separator should be PIPE"
    assert file_info.csv_use_end_time is True, "The csv_use_end_time should be True"

    file_info = FileInfo(path=resource_dir / "marker.lab")
    assert (
        file_info.csv_columns_separator == FileInfo.CsvColumnSeparators.TAB
    ), "The csv_columns_separator should be TAB"
    assert file_info.csv_use_end_time is True, "The csv_use_end_time should be True"

    with pytest.raises(TypeError):
        file_info = FileInfo(
            csv_columns_separator=FileInfo.CsvColumnSeparators.PIPE,
            csv_use_end_time=True,
        )

    with pytest.raises(ValueError):
        file_info = FileInfo(
            path=resource_dir / "marker.lab",
            csv_columns_separator=FileInfo.CsvColumnSeparators.PIPE,
            csv_use_end_time=True,
        )

    with pytest.raises(TypeError):
        file_info = FileInfo(
            path=resource_dir / "marker.json",
            csv_columns_separator=FileInfo.CsvColumnSeparators.PIPE,
            csv_use_end_time=True,
        )

    with pytest.raises(TypeError):
        file_info = FileInfo(
            path=resource_dir / "marker.cue",
            csv_columns_separator=FileInfo.CsvColumnSeparators.PIPE,
            csv_use_end_time=True,
        )

    with pytest.raises(TypeError):
        file_info = FileInfo(path=resource_dir / "Sound.wav")

    with pytest.raises(ValueError):
        file_info = FileInfo(path=resource_dir / "unexistant_marker.cue")

    file_info = FileInfo(path=resource_dir / "marker.cue")
    with pytest.raises(TypeError):
        file_info.csv_columns_separator = FileInfo.CsvColumnSeparators.PIPE

    file_info = FileInfo(path=resource_dir / "marker.cue")
    with pytest.raises(TypeError):
        file_info.csv_use_end_time = False
