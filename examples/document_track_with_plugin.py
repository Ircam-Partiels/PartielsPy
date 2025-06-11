from pathlib import Path

from partielspy import *

root = Path(__file__).parent

partiels = Partiels()

plugin_list = partiels.get_plugin_list()
print("plugin_list:")
print(plugin_list)

doc = Document()
group = Group("My Group")
track = Track("My Track")
track.plugin_key = PluginKey("partiels-vamp-plugins:partielsspectrogram", "energies")

group.add_track(track)
doc.add_group(group)

template_path = root / "templates" / "example.ptldoc"
Path(template_path).parent.mkdir(parents=True, exist_ok=True)
doc.save(template_path)
