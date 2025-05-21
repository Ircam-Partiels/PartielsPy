import os
import shutil
import subprocess
from pathlib import Path

from PartielsPy import ExportConfigImage, Partiels


def test_export_image_default():
    root = Path(__file__).resolve().parent.parent
    partiels = Partiels()
    export_config = ExportConfigImage()
    input = str(root / "tests/samples/Sound.wav")
    template = str(root / "src/PartielsPy/templates/factory.ptldoc")
    output = str(root / "tests/exports/factory/jpeg/")
    shutil.rmtree(output, ignore_errors=True)
    partiels.export(input, template, output, export_config)
    assert sorted(os.listdir(output)) == [
        "Sound Group 1_Spectrogram.jpeg",
        "Sound Group 2_Waveform.jpeg",
    ], "Exported files do not match with expected files."


def test_export_image_editing_arguments():
    root = Path(__file__).resolve().parent.parent
    partiels = Partiels()
    export_config = ExportConfigImage()
    input = str(root / "tests/samples/Sound.wav")
    template = str(root / "src/PartielsPy/templates/factory.ptldoc")
    output = str(root / "tests/exports/factory/jpeg/")
    export_config.adapt_to_sample_rate = True
    export_config.format = ExportConfigImage.Formats.PNG
    export_config.width = 2000
    export_config.height = 1200
    export_config.group_overlay = True
    output = str(root / "tests/exports/factory/png/")
    shutil.rmtree(output, ignore_errors=True)
    partiels.export(input, template, output, export_config)
    assert sorted(os.listdir(output)) == [
        "Sound Group 1.png",
        "Sound Group 2.png",
    ], "Exported files do not match with expected files."


def test_export_image_with_arguments():
    root = Path(__file__).resolve().parent.parent
    partiels = Partiels()
    input = str(root / "tests/samples/Sound.wav")
    template = str(root / "src/PartielsPy/templates/factory.ptldoc")
    output = str(root / "tests/exports/factory/png2/")
    export_config = ExportConfigImage(
        format=ExportConfigImage.Formats.PNG,
        width=200,
        height=200,
        group_overlay=True,
        adapt_to_sample_rate=True,
    )
    shutil.rmtree(output, ignore_errors=True)
    partiels.export(input, template, output, export_config)
    assert sorted(os.listdir(output)) == [
        "Sound Group 1.png",
        "Sound Group 2.png",
    ], "Exported files do not match with expected files."


def test_export_image_with_wrong_parameters():
    root = Path(__file__).resolve().parent.parent
    partiels = Partiels()
    input = str(root / "tests/samples/Sound.wav")
    template = str(root / "src/PartielsPy/templates/factory.ptldoc")
    output = str(root / "tests/exports/factory/error/")
    shutil.rmtree(output, ignore_errors=True)
    export_config = ExportConfigImage()
    try:
        export_config.format = "dummy"
        assert False, "ExportConfigImage didn't raise an error with unvalid format"
    except ValueError:
        pass

    export_config = ExportConfigImage()
    export_config.width = -100
    try:
        partiels.export(input, template, output, export_config)
    except subprocess.CalledProcessError as e:
        assert e.returncode != 0, "Export didn't fail with unvalid width"

    export_config = ExportConfigImage()
    export_config.height = -100
    try:
        partiels.export(input, template, output, export_config)
    except subprocess.CalledProcessError as e:
        assert e.returncode != 0, "Export didn't fail with unvalid height"

    assert (
        os.listdir(output) == []
    ), "Exported files should not exist with wrong parameters"


def test_export_image_without_vamp_path():
    root = Path(__file__).resolve().parent.parent
    partiels = Partiels()
    input = str(root / "tests/samples/Sound.wav")
    template = str(root / "src/PartielsPy/templates/factory.ptldoc")
    output = str(root / "tests/exports/factory/error/")
    shutil.rmtree(output, ignore_errors=True)
    export_config = ExportConfigImage()
    os.environ["VAMP_PATH"] = "/dummy/path/"
    try:
        partiels.export(input, template, output, export_config)
    except subprocess.CalledProcessError as e:
        assert e.returncode == 1, "Export didn't fail without a valid VAMP_PATH"

    assert (
        os.listdir(output) == []
    ), "Exported files should not exist with wrong parameters"
