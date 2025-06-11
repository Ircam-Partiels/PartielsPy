import copy
from pathlib import Path

from partielspy import *

root = Path(__file__).parent

doc = Document()
group = Group("My Group")
track = Track("My Track")

group.add_track(track)
doc.add_group(group)

group_copy = copy.deepcopy(group)
group_copy.name = "Updated Group Name"

track_copy = group_copy.tracks[0]
track_copy.name = "Updated Track Name"

track_copy_copy = copy.deepcopy(track_copy)
track_copy_copy.name = "Another Track Name"

group_copy.add_track(track_copy_copy)
doc.add_group(group_copy)

print(doc)
Partiels().save(doc, root / "templates/" / "example.xml")
