"""A class to manage plugin keys"""

from lxml import etree


class PluginKey:
    """
    This class is used to represent a key for a plugin.
    It contains an identifier and a feature, which are used to uniquely identify the key.
    Each :class:`partielspy.track` class has a plugin key associated with it.
    The plugin key is used to identify the plugin that is associated with the track.
    The get_plugin_list() method of the :class:`partielspy.partiels` class returns\
    a list of PluginKey based on all the available plugins.

    Args:
        identifier (str): the identifier of the key (default: "")
        feature (str): the feature of the key (default: "")
    """

    def __init__(self, identifier: str = "", feature: str = ""):
        self.__identifier = identifier
        self.__feature = feature

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def feature(self) -> str:
        return self.__feature

    def _from_xml(self, node: etree.Element):
        self.__identifier = node.get("identifier", self.__identifier)
        self.__feature = node.get("feature", self.__feature)

    def _to_xml(self) -> etree.Element:
        node = etree.Element("key")
        node.set("identifier", self.__identifier)
        node.set("feature", self.__feature)
        return node
