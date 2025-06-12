from lxml import etree

from .plugin_key import PluginKey


class PluginList(list[PluginKey]):
    @classmethod
    def _from_xml(cls, node: etree.Element):
        return cls(
            [
                PluginKey(key.get("identifier"), key.get("feature"))
                for plugin in node.findall("plugin")
                if (key := plugin.find("key")) is not None
            ]
        )

    def __str__(self):
        return "\n".join([f"{item.identifier}, {item.feature}" for item in self])
