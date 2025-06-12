from lxml import etree

from .plugin import Plugin


class Track:
    def __init__(self, name: str = "New Track"):
        self.__name = name
        self.__plugin = Plugin()

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

    def _to_xml(self, node: etree):
        node.set("name", self.__name)
        self.__plugin._to_xml(node)

    def _to_json(self) -> dict:
        res = {
            "name": self.__name,
            "plugin": self.__plugin._to_json(),
        }
        return res
