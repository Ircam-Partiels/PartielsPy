from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent
resource = root / "resource"

partiels = Partiels()

document = Document(audio_file_layout=resource / "Sound.wav")
group = Group("Group")
track = Track("Track")
track.file_info = FileInfo(resource / "marker.csv")
group.add_track(track)
document.add_group(group)

config = ExportConfig(format=ExportConfig.Formats.JSON)
output = root / "examples" / "exports" / "document_track_with_file"
partiels.export(document, output, config)
