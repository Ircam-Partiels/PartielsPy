import copy
from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent

document = Document(audio_file_layout=root / "resource" / "Sound.wav")
group = Group("My Group")
track = Track("My Track")

group.add_track(track)
document.add_group(group)

group_copy = copy.deepcopy(group)
group_copy.name = "Updated Group Name"

track_copy = group_copy.tracks[0]
track_copy.name = "Updated Track Name"

track_copy_copy = copy.deepcopy(track_copy)
track_copy_copy.name = "Another Track Name"

group_copy.add_track(track_copy_copy)
document.add_group(group_copy)

filepath = root / "examples" / "exports" / "documents" / "example.ptldoc"
Path(filepath).parent.mkdir(parents=True, exist_ok=True)
document.save(filepath)
