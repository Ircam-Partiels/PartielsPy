import shutil
from pathlib import Path

import pytest

from partielspy import *
from partielspy.export_config import ExportConfig

root = Path(__file__).parent

audio_file = root.parent / "resource" / "Sound.wav"


def test_basic_creation():
    doc = Document()
    group = Group("Test Group")
    assert group.name == "Test Group", "Group name should be 'Test Group'"
    assert len(group.tracks) == 0, "Group should initially have no tracks"
    track = Track("Test Track")
    assert track.name == "Test Track", "Track name should be 'Test Track'"
    group.add_track(track)
    assert len(group.tracks) == 1, "Group should have one track after adding"
    doc.add_group(group)
    assert len(doc.groups) == 1, "Document should have one group after adding"
    output = root / "templates" / "test_basic_creation.ptldoc"
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    assert output.exists(), "Output file was not created"
    group.remove_track(track)
    assert len(group.tracks) == 0, "Group should have no tracks after removal"
    doc.remove_group(group)
    assert len(doc.groups) == 0, "Document should have no groups after removal"


def test_basic_errors():
    doc = Document()
    group = Group("Group")
    track = Track("Track")

    with pytest.raises(TypeError, match="Expected a Group instance"):
        doc.add_group("dummy")
    with pytest.raises(TypeError, match="Expected a Track instance"):
        group.add_track("dummy")
    with pytest.raises(ValueError, match="Group not found in document"):
        doc.remove_group(group)
    with pytest.raises(ValueError, match="Track not found in group"):
        group.remove_track(track)
    doc.add_group(group)
    with pytest.raises(ValueError, match="Group already exists in document"):
        doc.add_group(group)
    group.add_track(track)
    with pytest.raises(ValueError, match="Track already exists in group"):
        group.add_track(track)


def test_load_save():
    input_file = root.parent / "templates" / "factory.ptldoc"
    output_file = root / "templates" / "test_load_save.ptldoc"

    doc = Document.load(input_file)
    assert len(doc.groups) > 0, "Document should have groups after loading"

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_file)
    assert output_file.exists(), "Output file was not created after saving"

    export_dir = root / "exports" / "test_load_save"
    expected_export_dir = export_dir / "expected"
    result_export_dir = export_dir / "result"
    expected_files = ["Sound Group 1_Spectrogram.csv", "Sound Group 2_Waveform.csv"]
    partiels = Partiels()
    config = ExportConfig(format=ExportConfig.Formats.CSV)
    document = Document.load(input_file)
    partiels.export(audio_file, document, expected_export_dir, config)
    document = Document.load(output_file)
    partiels.export(audio_file, document, result_export_dir, config)
    for expected_file in expected_files:
        expected_path = expected_export_dir / expected_file
        result_path = result_export_dir / expected_file
        assert expected_path.exists(), f"Expected file {expected_file} does not exist"
        assert result_path.exists(), f"Result file {expected_file} does not exist"
        with open(expected_path, "r") as ef, open(result_path, "r") as rf:
            assert ef.read() == rf.read(), f"File {expected_file} contents do not match"


def export_document_with_file(extension: str, config: ExportConfig):
    src = root.parent / "resource" / f"marker.{extension}"
    output = (
        root / "exports" / "file_result" / extension / f"Sound Group_Track.{extension}"
    )

    partiels = Partiels()
    document = Document()
    group = Group("Group")
    track = Track("Track")
    track.file_info = FileInfo(src)
    document.add_group(group)
    group.add_track(track)

    shutil.rmtree(output.parent, ignore_errors=True)
    partiels.export(audio_file, document, output.parent, config)

    with (
        open(src, "r") as ef,
        open(output, "r") as rf,
    ):
        assert ef.read() == rf.read(), f"File contents do not match for {extension}"


def test_document_with_file_csv():
    export_document_with_file("csv", ExportConfig(format=ExportConfig.Formats.CSV))


def test_document_with_file_lab():
    export_document_with_file("lab", ExportConfig(format=ExportConfig.Formats.LAB))


def test_document_with_file_json():
    export_document_with_file("json", ExportConfig(format=ExportConfig.Formats.JSON))


def test_document_with_file_cue():
    export_document_with_file("cue", ExportConfig(format=ExportConfig.Formats.CUE))
