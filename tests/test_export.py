import os
import shutil
import subprocess
from pathlib import Path

import pytest

from partielspy import *

root = Path(__file__).resolve().parent.parent
audiofile = root / "resource/Sound.wav"

template_factory = root / "templates/factory.ptldoc"
template_harmonic_partials_tracking = root / "templates/harmonic_partials_tracking.ptldoc"  # fmt: skip
template_waveform_fft = root / "templates/waveform_fft.ptldoc"
template_beat_detection = root / "templates/beat_detection.ptldoc"

expected_filenames_default = ["Sound Group 1", "Sound Group 2"]
expected_filenames_factory = ["Sound Group 1_Spectrogram", "Sound Group 2_Waveform"]
expected_filenames_waveform_fft = ["Sound Group 1_Fast Fourier Transform", "Sound Group 2_Waveform"]  # fmt: skip
expected_filenames_beat_detection = ["Sound Group 1_Beat Detection"]


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
        "Sound Group 1_Fast Fourier Transform",
        "Sound Group 1_Feature Scoring",
    ]
    for i in range(20):
        res.append(f"Sound Group 1_Partial {str(i + 1)}")
    res = [f"{file}.{extension}" for file in res]
    return sorted(res)


def test_export_image_default():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigImage()
    output = remove_and_get_output_folder(path="factory/jpeg")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="jpeg"
    ), "Exported files do not match with expected files."


def test_export_image_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigImage()
    export_config.adapt_to_sample_rate = True
    export_config.format = ExportConfigImage.Formats.PNG
    export_config.width = 2000
    export_config.height = 1200
    export_config.group_overlay = True
    output = remove_and_get_output_folder(path="factory/png")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_default, extension="png"
    ), "Exported files do not match with expected files."


def test_export_image_with_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigImage(
        format=ExportConfigImage.Formats.PNG,
        width=200,
        height=200,
        group_overlay=True,
        adapt_to_sample_rate=True,
    )
    output = remove_and_get_output_folder(path="factory/png2")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_default, extension="png"
    ), "Exported files do not match with expected files."


def test_export_image_with_wrong_parameters():
    partiels = Partiels()
    document = Document.load(template_factory)
    output = remove_and_get_output_folder(path="factory/error")
    export_config = ExportConfigImage()
    with pytest.raises(ValueError):
        export_config.format = "dummy"

    export_config = ExportConfigImage()
    export_config.width = -100
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(audiofile, document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with unvalid width"

    export_config = ExportConfigImage()
    export_config.height = -100
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(audiofile, document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with unvalid height"

    assert (
        os.listdir(output) == []
    ), "Exported files should not exist with wrong parameters"


def test_export_csv_default():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigCsv()
    output = remove_and_get_output_folder(path="factory/csv")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="csv"
    ), "Exported files do not match with expected files."


def test_export_csv_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigCsv()
    export_config.include_header = True
    export_config.columns_separator = ExportConfigCsv.Separators.SPACE
    export_config.ignore_matrix_tracks = True
    export_config.adapt_to_sample_rate = True
    output = remove_and_get_output_folder(path="factory/csv2")
    partiels.export(audiofile, document, output, export_config)
    expected = [
        get_expected_filenames(filenames=expected_filenames_factory, extension="csv")[1]
    ]
    assert (
        sorted(os.listdir(output)) == expected
    ), "Exported files do not match with expected files."


def test_export_csv_with_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigCsv(
        include_header=True,
        columns_separator=ExportConfigCsv.Separators.SPACE,
        ignore_matrix_tracks=True,
        adapt_to_sample_rate=True,
    )
    output = remove_and_get_output_folder(path="factory/csv3")
    partiels.export(audiofile, document, output, export_config)
    expected = get_expected_filenames(
        filenames=expected_filenames_factory, extension="csv"
    )
    assert sorted(os.listdir(output)) == [
        expected[1]
    ], "Exported files do not match with expected files."


def test_export_csv_with_wrong_parameters():
    export_config = ExportConfigCsv()
    with pytest.raises(ValueError):
        export_config.columns_separator = "dummy"


def test_export_reaper_default():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    export_config = ExportConfigReaper()
    output = remove_and_get_output_folder(path="beat_detection/reaper")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="csv"
    ), "Exported files do not match with expected files."


def test_export_reaper_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    export_config = ExportConfigReaper()
    export_config.reaper_type = ExportConfigReaper.ReaperTypes.MARKER
    export_config.adapt_to_sample_rate = True
    output = remove_and_get_output_folder(path="beat_detection/reaper2")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="csv"
    ), "Exported files do not match with expected files."


def test_export_reaper_with_arguments():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    export_config = ExportConfigReaper(
        reaper_type=ExportConfigReaper.ReaperTypes.MARKER, adapt_to_sample_rate=True
    )
    output = remove_and_get_output_folder(path="beat_detection/reaper3")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="csv"
    ), "Exported files do not match with expected files."


def test_export_reaper_with_no_marker_template():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigReaper()
    output = remove_and_get_output_folder(path="factory/reaper4")
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(audiofile, document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with no marker template"
    assert (
        sorted(os.listdir(output)) == []
    ), "Exported files do not match with expected files."


def test_export_reaper_with_wrong_parameters():
    export_config = ExportConfigReaper()
    with pytest.raises(ValueError):
        export_config.reaper_type = "dummy"


def test_export_lab_default():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigLab()
    output = remove_and_get_output_folder(path="factory/lab")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="lab"
    ), "Exported files do not match with expected files."


def test_export_lab_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigLab()
    export_config.adapt_to_sample_rate = True
    output = remove_and_get_output_folder(path="factory/lab2")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="lab"
    ), "Exported files do not match with expected files."


def test_export_lab_with_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigLab(adapt_to_sample_rate=True)
    output = remove_and_get_output_folder(path="factory/lab3")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="lab"
    ), "Exported files do not match with expected files."


def test_export_json_default():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigJson()
    output = remove_and_get_output_folder(path="factory/json")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="json"
    ), "Exported files do not match with expected files."


def test_export_json_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigJson()
    export_config.include_plugin_description = True
    export_config.ignore_matrix_tracks = True
    export_config.adapt_to_sample_rate = True
    output = remove_and_get_output_folder("factory/json2")
    partiels.export(audiofile, document, output, export_config)
    expected = get_expected_filenames(
        filenames=expected_filenames_factory, extension="json"
    )
    assert sorted(os.listdir(output)) == [
        expected[1]
    ], "Exported files do not match with expected files."


def test_export_json_with_arguments():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigJson(
        include_plugin_description=True,
        ignore_matrix_tracks=True,
        adapt_to_sample_rate=True,
    )
    output = remove_and_get_output_folder(path="factory/json2")
    partiels.export(audiofile, document, output, export_config)
    expected = get_expected_filenames(
        filenames=expected_filenames_factory, extension="json"
    )
    assert sorted(os.listdir(output)) == [
        expected[1]
    ], "Exported files do not match with expected files."


def test_export_cue_default():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    export_config = ExportConfigCue()
    output = remove_and_get_output_folder(path="beat_detection/cue")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="cue"
    ), "Exported files do not match with expected files."


def test_export_cue_editing_arguments():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    export_config = ExportConfigCue()
    export_config.ignore_matrix_tracks = False
    export_config.adapt_to_sample_rate = False
    output = remove_and_get_output_folder(path="beat_detection/cue2")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="cue"
    ), "Exported files do not match with expected files."


def test_export_cue_with_arguments():
    partiels = Partiels()
    document = Document.load(template_beat_detection)
    export_config = ExportConfigCue(
        ignore_matrix_tracks=False, adapt_to_sample_rate=False
    )
    output = remove_and_get_output_folder(path="beat_detection/cue3")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_beat_detection, extension="cue"
    ), "Exported files do not match with expected files."


def test_export_cue_with_no_marker_template():
    partiels = Partiels()
    document = Document.load(template_factory)
    export_config = ExportConfigCue()
    output = remove_and_get_output_folder(path="factory/cue4")
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(audiofile, document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with no marker template"
    assert (
        sorted(os.listdir(output)) == []
    ), "Exported files do not match with expected files."


def test_export_vamp_plugins():
    partiels = Partiels()
    document = Document.load(template_waveform_fft)
    export_config = ExportConfigImage()
    output = remove_and_get_output_folder(path="waveform_fft/jpeg")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_waveform_fft, extension="jpeg"
    ), "Exported files do not match with expected files."

    document = Document.load(template_harmonic_partials_tracking)
    export_config = ExportConfigJson()
    output = remove_and_get_output_folder(path="harmonic_partials_tracking/json")
    partiels.export(audiofile, document, output, export_config)
    assert sorted(
        os.listdir(output)
    ) == get_expected_filenames_harmonic_partials_tracking(
        "json"
    ), "Exported files do not match with expected files."


def test_export_image_with_wrong_vamp_path():
    partiels = Partiels()
    document = Document.load(template_factory)
    vamp_path = os.environ.get("VAMP_PATH", "")
    os.environ["VAMP_PATH"] = "/dummy/path/"
    output = remove_and_get_output_folder(path="factory/jpeg2")
    export_config = ExportConfigImage()
    partiels.export(audiofile, document, output, export_config)
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
    vamp_path = os.environ.get("VAMP_PATH", "")
    os.environ["VAMP_PATH"] = "/dummy/path/"
    output = remove_and_get_output_folder(path="waveform_fft/error")
    export_config = ExportConfigImage()
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        partiels.export(audiofile, document, output, export_config)
    assert excinfo.value.returncode != 0, "Export didn't fail with wrong VAMP_PATH"
    assert (
        sorted(os.listdir(output)) == []
    ), "Exported files should not exist with wrong VAMP_PATH"
    assert (
        os.environ.get("VAMP_PATH") == "/dummy/path/"
    ), "VAMP_PATH should not be changed."
    os.environ["VAMP_PATH"] = vamp_path
