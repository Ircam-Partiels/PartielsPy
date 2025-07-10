import os
import shutil
import subprocess
from pathlib import Path

import pytest

from partielspy import *

root = Path(__file__).resolve().parent.parent
audio_file = root / "resource" / "Sound.wav"

template_factory = root / "templates/factory.ptldoc"
template_harmonic_partials_tracking = root / "templates/harmonic_partials_tracking.ptldoc"  # fmt: skip
template_waveform_fft = root / "templates/waveform_fft.ptldoc"
template_beat_detection = root / "templates/beat_detection.ptldoc"

expected_filenames_default = ["Group 1", "Group 2"]
expected_filenames_factory = ["Group 1_Spectrogram", "Group 2_Waveform"]
expected_filenames_waveform_fft = ["Group 1_Fast Fourier Transform", "Group 2_Waveform"]  # fmt: skip
expected_filenames_beat_detection = ["Group 1_Beat Detection"]


def remove_and_get_output_folder(path):
    res = str(root / "tests" / "exports" / path)
    shutil.rmtree(res, ignore_errors=True)
    return res


def get_expected_filenames(filenames, extension):
    res = []
    for name in filenames:
        res.append(f"{name}.{extension}")
    return res


def get_expected_filenames_harmonic_partials_tracking(extension):
    res = [
        "Group 1_Fast Fourier Transform",
        "Group 1_Feature Scoring",
    ]
    for i in range(20):
        res.append(f"Group 1_Partial {str(i + 1)}")
    res = [f"{file}.{extension}" for file in res]
    return sorted(res)


def test_export_image_default():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    output = remove_and_get_output_folder(path="factory/jpeg")
    partiels.export(document, output, ExportConfig(format=ExportConfig.Formats.JPEG))
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="jpeg"
    ), "Exported files do not match with expected files."


def test_export_image_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.JPEG)
    export_config.format = ExportConfig.Formats.PNG
    export_config.image_width = 2000
    export_config.image_height = 1200
    export_config.image_group_overlay = True
    export_config.image_ppi = 100
    output = remove_and_get_output_folder(path="factory/png")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_default, extension="png"
    ), "Exported files do not match with expected files."


def test_export_image_with_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(
        format=ExportConfig.Formats.PNG,
        image_width=200,
        image_height=200,
        image_group_overlay=True,
        image_ppi=100,
    )
    output = remove_and_get_output_folder(path="factory/png2")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_default, extension="png"
    ), "Exported files do not match with expected files."


def test_export_image_with_wrong_parameters():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    output = remove_and_get_output_folder(path="factory/error")
    export_config = ExportConfig(format=ExportConfig.Formats.JPEG)
    with pytest.raises(ValueError):
        export_config.format = "dummy"

    export_config = ExportConfig(format=ExportConfig.Formats.JPEG)
    export_config.image_width = -100
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with invalid width"

    export_config = ExportConfig(format=ExportConfig.Formats.JPEG)
    export_config.image_height = -100
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with invalid height"

    assert (
        os.listdir(output) == []
    ), "Exported files should not exist with wrong parameters"


def test_export_csv_default():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.CSV)
    output = remove_and_get_output_folder(path="factory/csv")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="csv"
    ), "Exported files do not match with expected files."


def test_export_csv_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.CSV)
    export_config.csv_include_header = True
    export_config.csv_columns_separator = ExportConfig.CsvColumnSeparators.SPACE
    export_config.ignore_matrix_tracks = True
    output = remove_and_get_output_folder(path="factory/csv2")
    partiels.export(document, output, export_config)
    expected = [
        get_expected_filenames(filenames=expected_filenames_factory, extension="csv")[1]
    ]
    assert (
        sorted(os.listdir(output)) == expected
    ), "Exported files do not match with expected files."


def test_export_csv_with_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(
        format=ExportConfig.Formats.CSV,
        csv_include_header=True,
        csv_columns_separator=ExportConfig.CsvColumnSeparators.SPACE,
        ignore_matrix_tracks=True,
    )
    output = remove_and_get_output_folder(path="factory/csv3")
    partiels.export(document, output, export_config)
    expected = get_expected_filenames(
        filenames=expected_filenames_factory, extension="csv"
    )
    assert sorted(os.listdir(output)) == [
        expected[1]
    ], "Exported files do not match with expected files."


def test_export_csv_with_wrong_parameters():
    export_config = ExportConfig(format=ExportConfig.Formats.CSV)
    with pytest.raises(ValueError):
        export_config.csv_columns_separator = "dummy"


def test_export_reaper_default():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.REAPER)
    output = remove_and_get_output_folder(path="beat_detection/reaper")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="csv"
    ), "Exported files do not match with expected files."


def test_export_reaper_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.REAPER)
    export_config.reaper_type = ExportConfig.ReaperTypes.MARKER
    output = remove_and_get_output_folder(path="beat_detection/reaper2")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="csv"
    ), "Exported files do not match with expected files."


def test_export_reaper_with_arguments():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(
        format=ExportConfig.Formats.REAPER,
        reaper_type=ExportConfig.ReaperTypes.MARKER,
    )
    output = remove_and_get_output_folder(path="beat_detection/reaper3")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="csv"
    ), "Exported files do not match with expected files."


def test_export_reaper_with_no_marker_template():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.REAPER)
    output = remove_and_get_output_folder(path="factory/reaper4")
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with no marker template"
    assert (
        sorted(os.listdir(output)) == []
    ), "Exported files do not match with expected files."


def test_export_reaper_with_wrong_parameters():
    export_config = ExportConfig(format=ExportConfig.Formats.REAPER)
    with pytest.raises(ValueError):
        export_config.reaper_type = "dummy"


def test_export_lab_default():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.LAB)
    output = remove_and_get_output_folder(path="factory/lab")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="lab"
    ), "Exported files do not match with expected files."


def test_export_lab_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.LAB)
    output = remove_and_get_output_folder(path="factory/lab2")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="lab"
    ), "Exported files do not match with expected files."


def test_export_lab_with_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.LAB)
    output = remove_and_get_output_folder(path="factory/lab3")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="lab"
    ), "Exported files do not match with expected files."


def test_export_json_default():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.JSON)
    output = remove_and_get_output_folder(path="factory/json")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="json"
    ), "Exported files do not match with expected files."


def test_export_json_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.JSON)
    export_config.json_include_plugin_description = True
    export_config.ignore_matrix_tracks = True
    output = remove_and_get_output_folder("factory/json2")
    partiels.export(document, output, export_config)
    expected = get_expected_filenames(
        filenames=expected_filenames_factory, extension="json"
    )
    assert sorted(os.listdir(output)) == [
        expected[1]
    ], "Exported files do not match with expected files."


def test_export_json_with_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(
        format=ExportConfig.Formats.JSON,
        json_include_plugin_description=True,
        ignore_matrix_tracks=True,
    )
    output = remove_and_get_output_folder(path="factory/json2")
    partiels.export(document, output, export_config)
    expected = get_expected_filenames(
        filenames=expected_filenames_factory, extension="json"
    )
    assert sorted(os.listdir(output)) == [
        expected[1]
    ], "Exported files do not match with expected files."


def test_export_cue_default():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.CUE)
    output = remove_and_get_output_folder(path="beat_detection/cue")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="cue"
    ), "Exported files do not match with expected files."


def test_export_cue_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.CUE)
    export_config.ignore_matrix_tracks = False
    output = remove_and_get_output_folder(path="beat_detection/cue2")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="cue"
    ), "Exported files do not match with expected files."


def test_export_cue_with_arguments():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(
        format=ExportConfig.Formats.CUE,
        ignore_matrix_tracks=False,
    )
    output = remove_and_get_output_folder(path="beat_detection/cue3")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="cue"
    ), "Exported files do not match with expected files."


def test_export_cue_with_no_marker_template():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.CUE)
    output = remove_and_get_output_folder(path="factory/cue4")
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with no marker template"
    assert (
        sorted(os.listdir(output)) == []
    ), "Exported files do not match with expected files."


def test_export_vamp_plugins():
    partiels = Partiels()
    document = Document.load(template_waveform_fft)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.JPEG)
    output = remove_and_get_output_folder(path="waveform_fft/jpeg")
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_waveform_fft, extension="jpeg"
    ), "Exported files do not match with expected files."

    document = Document.load(template_harmonic_partials_tracking)
    document.audio_file_layout = audio_file
    export_config = ExportConfig(format=ExportConfig.Formats.JSON)
    output = remove_and_get_output_folder(path="harmonic_partials_tracking/json")
    partiels.export(document, output, export_config)
    assert sorted(
        os.listdir(output)
    ) == get_expected_filenames_harmonic_partials_tracking(
        "json"
    ), "Exported files do not match with expected files."


def test_export_image_with_wrong_vamp_path():
    partiels = Partiels()
    document = Document.load(template_factory)
    document.audio_file_layout = audio_file
    vamp_path = os.environ.get("VAMP_PATH", "")
    os.environ["VAMP_PATH"] = "/dummy/path/"
    output = remove_and_get_output_folder(path="factory/jpeg2")
    export_config = ExportConfig(format=ExportConfig.Formats.JPEG)
    partiels.export(document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="jpeg"
    ), "Exported files do not match with expected files."
    assert (
        os.environ.get("VAMP_PATH") == "/dummy/path/"
    ), "VAMP_PATH should not be changed."
    os.environ["VAMP_PATH"] = vamp_path


def test_export_vamp_plugins_with_wrong_vamp_path():
    partiels = Partiels()
    document = Document.load(template_waveform_fft)
    document.audio_file_layout = audio_file
    vamp_path = os.environ.get("VAMP_PATH", "")
    os.environ["VAMP_PATH"] = "/dummy/path/"
    output = remove_and_get_output_folder(path="waveform_fft/error")
    export_config = ExportConfig(format=ExportConfig.Formats.JPEG)
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with wrong VAMP_PATH"
    assert (
        sorted(os.listdir(output)) == []
    ), "Exported files should not exist with wrong VAMP_PATH"
    assert (
        os.environ.get("VAMP_PATH") == "/dummy/path/"
    ), "VAMP_PATH should not be changed."
    os.environ["VAMP_PATH"] = vamp_path
