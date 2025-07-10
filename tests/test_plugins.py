import logging
import os
import shutil
import subprocess
from pathlib import Path

from partielspy import *


def test_plugin_list():
    expected = [
        ["partiels-vamp-plugins:partielsnewtrack", "markers"],
        ["partiels-vamp-plugins:partielsnewtrack", "points"],
        ["partiels-vamp-plugins:partielsspectrogram", "energies"],
        ["partiels-vamp-plugins:partielswaveform", "peaks"],
    ]
    os.environ["VAMP_PATH"] = "dummy/path"
    plugin_list = Partiels().get_plugin_list()
    for i, item in enumerate(plugin_list):
        assert isinstance(item, PluginKey), f"Item {i} is not a PluginKey"
        assert item.identifier == expected[i][0], f"Item {i} identifier mismatch"
        assert item.feature == expected[i][1], f"Item {i} feature mismatch"


def test_create_document_with_factory_plugins():
    root = Path(__file__).parent
    exported_filename = "Group 2_Waveform.csv"
    audio_file_path = root.parent / "resource" / "Sound.wav"
    export_output_dir = root / "exports" / "test_factory_creation"

    # Remove the export directory
    shutil.rmtree(export_output_dir, ignore_errors=True)

    # Initialize Partiels instance
    partiels = Partiels()

    # Create the reference document
    document_ref = Document.load(root.parent / "templates" / "factory.ptldoc")
    document_ref.audio_file_layout = audio_file_path

    # Export the reference document to the reference directory
    try:
        partiels.export(
            document_ref,
            export_output_dir / "reference",
            ExportConfig(format=ExportConfig.Formats.CSV),
        )
    except subprocess.CalledProcessError as e:
        logging.getLogger(__name__).error(e.stderr)
        assert False, f"Export failed: {e}"

    reference_file = export_output_dir / "reference" / exported_filename

    # Create the result document
    document_res = Document(audio_file_path)

    # Create a first group and add a spectrogram track
    group1 = Group("Group 1")
    track1 = Track("Spectrogram")
    track1.plugin_key = PluginKey(
        "partiels-vamp-plugins:partielsspectrogram", "energies"
    )
    group1.add_track(track1)
    document_res.add_group(group1)

    # Create a second group and add a waveform track
    group2 = Group("Group 2")
    track2 = Track("Waveform")
    track2.plugin_key = PluginKey("partiels-vamp-plugins:partielswaveform", "peaks")
    group2.add_track(track2)
    document_res.add_group(group2)

    # Export the result document to the result directory
    try:
        partiels.export(
            document_res,
            export_output_dir / "result",
            ExportConfig(format=ExportConfig.Formats.CSV),
        )
    except subprocess.CalledProcessError as e:
        logging.getLogger(__name__).error(e.stderr)
        assert False, f"Export failed: {e}"
    result_file = export_output_dir / "result" / exported_filename

    assert reference_file.exists(), f"Reference file {reference_file} does not exist"
    assert result_file.exists(), f"Result file {result_file} does not exist"
    with open(reference_file, "r") as ef, open(result_file, "r") as rf:
        assert ef.read() == rf.read(), f"Content mismatch for {exported_filename}"
