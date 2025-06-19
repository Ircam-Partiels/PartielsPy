import os
from pathlib import Path

from partielspy import *
from partielspy.plugin.plugin import Plugin

root = Path(__file__).parent
audio_file = root.parent / "resource" / "Sound.wav"
template_factory = root.parent / "templates" / "factory.ptldoc"


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
        assert isinstance(item, Plugin), f"Item {i} is not a Plugin"
        assert item.key.identifier == expected[i][0], f"Item {i} identifier mismatch"
        assert item.key.feature == expected[i][1], f"Item {i} feature mismatch"


def test_create_document_with_factory_plugins():
    partiels = Partiels()

    plugin_list = partiels.get_plugin_list()
    doc = Document()

    group1 = Group("Group 1")
    track1 = Track("Spectrogram")
    track1.plugin = plugin_list.get(
        "partiels-vamp-plugins:partielsspectrogram", "energies"
    )
    group1.add_track(track1)
    doc.add_group(group1)

    group2 = Group("Group 2")
    track2 = Track("Waveform")
    track2.plugin = plugin_list.get("partiels-vamp-plugins:partielswaveform", "peaks")
    group2.add_track(track2)
    doc.add_group(group2)

    template_output_dir = root / "templates"
    template_output = template_output_dir / "test_factory_creation.ptldoc"
    if not template_output_dir.exists():
        os.mkdir(template_output_dir)
    with open(template_output, "wb") as f:
        doc.save(f)
    export_output = root / "exports" / "test_factory_creation"
    export_output_expected = export_output / "expected"
    export_output_result = export_output / "result"
    export_config = ExportConfigCsv()
    partiels.export(audio_file, template_factory, export_output_expected, export_config)
    partiels.export(audio_file, template_output, export_output_result, export_config)

    exported_filename = "Sound Group 2_Waveform.csv"

    expected_file = export_output_expected / exported_filename
    result_file = export_output_result / exported_filename
    assert expected_file.exists(), f"Expected file {expected_file} does not exist"
    assert result_file.exists(), f"Result file {result_file} does not exist"
    with open(expected_file, "r") as ef, open(result_file, "r") as rf:
        assert ef.read() == rf.read(), f"Content mismatch for {exported_filename}"
