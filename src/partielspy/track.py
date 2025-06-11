import copy

from lxml import etree

from .plugin_key import PluginKey
from .version import Version


class Track:
    def __init__(self, name: str = "New Track"):
        self.__xml_node = etree.Element("tracks")
        self.__name = name
        self.__plugin_key = PluginKey()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def plugin_key(self) -> PluginKey:
        return self.__plugin_key

    @plugin_key.setter
    def plugin_key(self, value: PluginKey):
        if not isinstance(value, PluginKey):
            raise TypeError("plugin_key must be an instance of PluginKey")
        self.__plugin_key = value

    def _from_xml(self, node: etree.Element):
        self.name = node.get("name", self.name)
        plugin_key_node = node.find("key")
        self.plugin_key._from_xml(plugin_key_node)
        node.remove(plugin_key_node)
        self.__xml_node = copy.deepcopy(node)

    def _to_xml(self, identifier: str) -> etree.Element:
        node = copy.deepcopy(self.__xml_node)
        node.set("MiscModelVersion", Version.get_compatibility_version_int())
        node.set("name", self.__name)
        node.set("identifier", identifier)
        node.append(self.__plugin_key._to_xml())
        return node
