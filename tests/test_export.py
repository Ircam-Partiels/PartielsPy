import os
import shutil
import subprocess
from pathlib import Path

from PartielsPy import ExportConfigImage, Partiels

root = Path(__file__).resolve().parent.parent
audiofile = root / "tests/samples/Sound.wav"

template_factory = root / "src/PartielsPy/templates/factory.ptldoc"

expected_filenames_default = ["Sound Group 1", "Sound Group 2"]
expected_filenames_factory = ["Sound Group 1_Spectrogram", "Sound Group 2_Waveform"]


def remove_and_get_output_folder(path):
    res = str(root / "tests" / "exports" / path)
    shutil.rmtree(res, ignore_errors=True)
    return res


def get_expected_filenames(filenames, extension):
    res = []
    for name in filenames:
        res.append(f"{name}.{extension}")
    return res


def test_export_image_default():
    partiels = Partiels()
    export_config = ExportConfigImage()
    output = remove_and_get_output_folder(path="factory/jpeg")
    partiels.export(audiofile, template_factory, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_factory, extension="jpeg"
    ), "Exported files do not match with expected files."


def test_export_image_editing_arguments():
    partiels = Partiels()
    export_config = ExportConfigImage()
    export_config.adapt_to_sample_rate = True
    export_config.format = ExportConfigImage.Formats.PNG
    export_config.width = 2000
    export_config.height = 1200
    export_config.group_overlay = True
    output = remove_and_get_output_folder(path="factory/png")
    partiels.export(audiofile, template_factory, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_default, extension="png"
    ), "Exported files do not match with expected files."


def test_export_image_with_arguments():
    partiels = Partiels()
    export_config = ExportConfigImage(
        format=ExportConfigImage.Formats.PNG,
        width=200,
        height=200,
        group_overlay=True,
        adapt_to_sample_rate=True,
    )
    output = remove_and_get_output_folder(path="factory/png2")
    partiels.export(audiofile, template_factory, output, export_config)
    assert sorted(os.listdir(output)) == get_expected_filenames(
        filenames=expected_filenames_default, extension="png"
    ), "Exported files do not match with expected files."


def test_export_image_with_wrong_parameters():
    partiels = Partiels()
    output = remove_and_get_output_folder(path="factory/error")
    export_config = ExportConfigImage()
    try:
        export_config.format = "dummy"
        assert False, "ExportConfigImage didn't raise an error with unvalid format"
    except ValueError:
        pass

    export_config = ExportConfigImage()
    export_config.width = -100
    try:
        partiels.export(audiofile, template_factory, output, export_config)
    except subprocess.CalledProcessError as e:
        assert e.returncode != 0, "Export didn't fail with unvalid width"

    export_config = ExportConfigImage()
    export_config.height = -100
    try:
        partiels.export(audiofile, template_factory, output, export_config)
    except subprocess.CalledProcessError as e:
        assert e.returncode != 0, "Export didn't fail with unvalid height"

    assert (
        os.listdir(output) == []
    ), "Exported files should not exist with wrong parameters"


def test_export_image_without_vamp_path():
    partiels = Partiels()
    output = remove_and_get_output_folder(path="factory/error")
    export_config = ExportConfigImage()
    vamp_path = os.environ.get("VAMP_PATH", "")
    print("vamp_path:", vamp_path)
    os.environ["VAMP_PATH"] = "/dummy/path/"
    try:
        partiels.export(audiofile, template_factory, output, export_config)
    except subprocess.CalledProcessError as e:
        assert e.returncode == 1, "Export didn't fail without a valid VAMP_PATH"
    print(str(vamp_path))
    os.environ["VAMP_PATH"] = vamp_path
    assert (
        os.listdir(output) == []
    ), "Exported files should not exist with wrong parameters"
