from pathlib import Path

from partielspy import *

folder = Path(__file__).parent
resource = folder.parent / "resource"

partiels = Partiels()

document = Document()
group = Group("Group")
track = Track("Track")
track.file_info = FileInfoCsv(resource / "marker.csv")
group.add_track(track)
document.add_group(group)

audio_file = resource / "Sound.wav"
config = ExportConfigJson()
output = folder / "exports" / "document_track_with_file"
partiels.export(audio_file, document, output, config)
