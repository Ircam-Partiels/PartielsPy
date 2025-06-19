from lxml import etree

from .plugin.plugin import Plugin
from .xml_element import XmlElement


class Track(XmlElement):
    __ignored_attributes = ["identifier", "name"]
    __ignored_children = ["key"]

    def __init__(self, name: str = "New Track"):
        self.__name = name
        self.__plugin = Plugin()
        super().__init__(
            ignored_attributes=Track.__ignored_attributes,
            ignored_children=Track.__ignored_children,
        )

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def plugin(self) -> Plugin:
        return self.__plugin

    @plugin.setter
    def plugin(self, value: Plugin):
        if not isinstance(value, Plugin):
            raise TypeError("plugin must be an instance of Plugin")
        self.__plugin = value

    @classmethod
    def _from_xml(cls, node: etree):
        track = cls()
        track.from_xml(node)
        track.name = node.get("name", "New Track")
        plugin_key_node = node.find("key")
        if plugin_key_node is not None:
            track.plugin = Plugin._from_xml(plugin_key_node)
        return track

    def _to_xml(self, node: etree):
        super().to_xml(node)
        node.set("name", self.__name)
        self.__plugin._to_xml(node)

    def _to_json(self) -> dict:
        res = {
            "name": self.__name,
            "plugin": self.__plugin._to_json(),
        }
        return res
