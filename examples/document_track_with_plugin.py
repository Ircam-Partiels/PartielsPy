from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent
resource = root.parent / "resource"

partiels = Partiels()

plugin_list = partiels.get_plugin_list()
print("plugin_list:")
print(plugin_list)

document = Document(audio_file_layout=resource / "Sound.wav")
group = Group("My Group")
track = Track("My Track")
track.plugin_key = PluginKey("partiels-vamp-plugins:partielsspectrogram", "energies")

group.add_track(track)
document.add_group(group)

template_path = (
    root / "examples" / "exports" / "documents" / "document_with_plugins.ptldoc"
)
Path(template_path).parent.mkdir(parents=True, exist_ok=True)
document.save(template_path)
