from pathlib import Path

from partielspy import *

root = Path(__file__).parent

partiels = Partiels()

plugin_list = partiels.plugin_list()
print(plugin_list)

doc = Document()
group = Group("My Group")
track = Track("My Track", plugin_list[0])

group.add_track(track)
doc.add_group(group)

print(doc)
template_path = root / "templates" / "example.ptldoc"
partiels.save(doc, template_path)
