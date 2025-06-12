"""A class to display the list of available plugins in Partiels"""

from lxml import etree

from .plugin_key import PluginKey


class PluginList(list[PluginKey]):
    """
    This class is not intended to be instantiated directly, but rather through the
    get_plugin_list method of the :class:`Partiels <partielspy.partiels>` class.
    It contains a list of :class:`PluginKey <partielspy.plugin_key>`,
    each representing a plugin key with an identifier and a feature.
    Its purpose is to provide a convenient way to access and display the list of plugins.

    Example usage:
        from partielspy import Partiels\n
        partiels = Partiels()\n
        plugin_list = partiels.get_plugin_list()\n
        print(plugin_list)
    """

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
        """Return a string representation of the plugin list"""
        return "\n".join([f"{item.identifier}, {item.feature}" for item in self])
