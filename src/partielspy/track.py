from lxml import etree

from .plugin_key import PluginKey


class Track:
    def __init__(self, name: str = "New Track", key: PluginKey = PluginKey()):
        self.__name = name
        self.__key = key

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def key(self) -> PluginKey:
        return self.__key

    @key.setter
    def key(self, value: PluginKey):
        if not isinstance(value, PluginKey):
            raise TypeError("key must be an instance of PluginKey")
        self.__key = value

    def _to_xml(self, node: etree):
        node.set("name", self.__name)
        key_node = etree.SubElement(node, "key")
        self.__key._to_xml(key_node)

    def __str__(self):
        return self.__name + " -> Plugin: " + str(self.__key)
