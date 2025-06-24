from pathlib import Path

from partielspy import *

folder = Path(__file__).parent

partiels = Partiels()

doc = Document()
group = Group("Group")
track = Track("Track")
track.file_info = FileInfoCsv(
    Path(folder / "results" / "document_with_file" / "src.csv")
)
group.add_track(track)
doc.add_group(group)

template = folder / "templates" / "doc_with_file_csv.ptldoc"
Path(template).parent.mkdir(parents=True, exist_ok=True)
doc.save(template)

audio_file = folder.parent / "resource" / "Sound.wav"
config = ExportConfigCsv()
output = folder / "exports" / "document_with_file"
partiels.export(audio_file, template, output, config)
