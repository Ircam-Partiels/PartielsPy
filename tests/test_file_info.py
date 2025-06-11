from pathlib import Path

import pytest

from partielspy import *

resource_dir = Path(__file__).resolve().parent.parent / "resource"


def test_file_info_creation():
    file_info = FileInfo()

    file_info = FileInfo(path=resource_dir / "marker.cue")
    assert file_info.columns_separator is None, "The columns_separator should be None"
    assert file_info.use_end_time is None, "The use_end_time should be None"

    file_info = FileInfo(path=resource_dir / "marker.csv")
    assert (
        file_info.columns_separator == FileInfo.Separators.COMMA
    ), "The columns_separator should be COMMA"
    assert file_info.use_end_time is False, "The use_end_time should be False"

    file_info = FileInfo(
        path=resource_dir / "marker.csv",
        columns_separator=FileInfo.Separators.PIPE,
        use_end_time=True,
    )
    assert (
        file_info.columns_separator == FileInfo.Separators.PIPE
    ), "The columns_separator should be PIPE"
    assert file_info.use_end_time is True, "The use_end_time should be True"

    file_info = FileInfo(path=resource_dir / "marker.lab")
    assert (
        file_info.columns_separator == FileInfo.Separators.TAB
    ), "The columns_separator should be TAB"
    assert file_info.use_end_time is True, "The use_end_time should be True"

    with pytest.raises(TypeError):
        file_info = FileInfo(
            columns_separator=FileInfo.Separators.PIPE, use_end_time=True
        )

    with pytest.raises(ValueError):
        file_info = FileInfo(
            path=resource_dir / "marker.lab",
            columns_separator=FileInfo.Separators.PIPE,
            use_end_time=True,
        )

    with pytest.raises(TypeError):
        file_info = FileInfo(
            path=resource_dir / "marker.json",
            columns_separator=FileInfo.Separators.PIPE,
            use_end_time=True,
        )

    with pytest.raises(TypeError):
        file_info = FileInfo(
            path=resource_dir / "marker.cue",
            columns_separator=FileInfo.Separators.PIPE,
            use_end_time=True,
        )

    with pytest.raises(TypeError):
        file_info = FileInfo(path=resource_dir / "Sound.wav")

    with pytest.raises(ValueError):
        file_info = FileInfo(path=resource_dir / "unexistant_marker.cue")

    file_info = FileInfo(path=resource_dir / "marker.cue")
    with pytest.raises(TypeError):
        file_info.columns_separator = FileInfo.Separators.PIPE

    file_info = FileInfo(path=resource_dir / "marker.cue")
    with pytest.raises(TypeError):
        file_info.use_end_time = False
