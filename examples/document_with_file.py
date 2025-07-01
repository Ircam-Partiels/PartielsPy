from pathlib import Path

from partielspy import *

folder = Path(__file__).parent

partiels = Partiels()

document = Document()
group = Group("Group")
track = Track("Track")
track.file_info = FileInfoCsv(
    Path(folder / "results" / "document_with_file" / "src.csv")
)
group.add_track(track)
document.add_group(group)

audio_file = folder.parent / "resource" / "Sound.wav"
config = ExportConfigCsv()
output = folder / "exports" / "document_with_file"
partiels.export(audio_file, document, output, config)
