import json

from .plugin_key import PluginKey


class PluginList(list):
    def __init__(self, chunk: str = None):
        data = json.loads(chunk)
        if not isinstance(data, dict):
            raise TypeError("The output of the command is not a dictionary")
        for plugin in data.get("plugins", []):
            super().append(
                PluginKey(
                    identifier=plugin.get("identifier", ""),
                    feature=plugin.get("feature", ""),
                )
            )

    def __str__(self):
        res = ""
        i = 0
        for item in self:
            res += "[" + str(i) + "] "
            res += str(item)
            res += "\n" if i < len(self) - 1 else ""
            i += 1
        return res
