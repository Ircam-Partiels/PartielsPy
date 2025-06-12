from pathlib import Path

from partielspy import *

root = Path(__file__).parent

partiels = Partiels()

plugin_list = partiels.get_plugin_list()
print("plugin_list:")
print(plugin_list)

vamp_plugin_list = plugin_list.get_matching_plugins("partiels-vamp-plugins")
print("vamp_plugin_list:")
print(vamp_plugin_list.to_json())

doc = Document()
group = Group("My Group")
track = Track("My Track")
track.plugin = plugin_list.get("partiels-vamp-plugins:partielsspectrogram", "energies")

group.add_track(track)
doc.add_group(group)

print(doc.to_json())
template_path = root / "templates" / "example.ptldoc"
with open(root / "templates" / "example.xml", "wb") as f:
    doc.save(f)
