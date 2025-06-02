import os
import shutil
import subprocess
from pathlib import Path

from PartielsPy import Document, ExportConfigImage, Group, Partiels, Track

root = Path(__file__).resolve().parent.parent
audiofile = root / "tests/samples/Sound.wav"


def test_plugin_list():
    partiels = Partiels()
    plugins = partiels.plugin_list
    assert isinstance(plugins, list)
    assert len(plugins) > 0


def test_document_from_ptldoc():
    partiels = Partiels()
    doc_in = root / "src/PartielsPy/templates/factory.ptldoc"
    doc_out = root / "tests/templates/loaded_document.ptldoc"
    document = Document.from_ptldoc(doc_in)
    document.save(doc_out)
    config = ExportConfigImage()
    export_in = root / "tests/exports/diff/in"
    export_out = root / "tests/exports/diff/out"
    partiels.export(audiofile, doc_in, export_in, config)
    partiels.export(audiofile, doc_out, export_out, config)
    ret = subprocess.run(
        ["diff", str(export_in), str(export_out)], capture_output=True, text=True
    )
    print(ret.stdout)


"""
def test_save_document():
    partiels = Partiels()
    document = Document()
    output_path = root / "tests/templates/saved_document.ptldoc"
    partiels.save(output_path, document)



def test_create_template():
    partiels = Partiels()
    document = Document()
    group = Group("Group 1")
    plugin = partiels.plugin_list[11]
    track = Track(
        plugin.identifier + "-" + plugin.feature, plugin.identifier, plugin.feature
    )
    group.addTrack(track)
    plugin = partiels.plugin_list[14]
    track = Track(
        plugin.identifier + "-" + plugin.feature, plugin.identifier, plugin.feature
    )
    group.addTrack(track)
    document.addGroup(group)
    root = Path(__file__).resolve().parent.parent
    output_folder = str(root / "tests/templates/generated")
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)
    template_path = output_folder + "/basic_template.ptldoc"
    document.save(template_path)


def test_export_template():
    partiels = Partiels()
    root = Path(__file__).resolve().parent.parent
    template_path = str(root / "tests/templates/generated/basic_template.ptldoc")
    audiofile_path = str(root / "tests/samples/Sound.wav")
    output = str(root / "tests/exports/basic_template")
    export_config = ExportConfigImage()
    shutil.rmtree(output, ignore_errors=True)
    partiels.export(audiofile_path, template_path, output, export_config)
    assert os.path.exists(output)
"""
