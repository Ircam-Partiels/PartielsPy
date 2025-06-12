import json

from .plugin import Plugin
from .plugin_key import PluginKey


class PluginList(list[Plugin]):
    @classmethod
    def from_json(cls, data: json):
        plugin_list = cls()
        for plugin in data:
            plugin_list.append(Plugin(PluginKey.from_json(plugin.get("key", ""))))
        return plugin_list

    def to_json(self) -> dict:
        return [plugin._to_json() for plugin in self]

    def get(self, identifier: str, feature: str) -> Plugin | None:
        for plugin in self:
            key = plugin.key
            if key.identifier == identifier and key.feature == feature:
                return plugin
        return None

    def get_matching_plugins(self, term_to_look_for: str) -> "PluginList":
        res = PluginList()
        for plugin in self:
            key = plugin.key
            if term_to_look_for in key.identifier or term_to_look_for in key.feature:
                res.append(plugin)
        return res

    def __str__(self):
        return "\n".join(
            [f"{item.key.identifier}, {item.key.feature}" for item in self]
        )
