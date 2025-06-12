from lxml import etree

from .plugin_key import PluginKey


class Track:
    def __init__(self, name: str = "New Track", key: PluginKey = PluginKey()):
        self.__name = name
        self.__key = key
        self.__xml_attributes = {}
        self.__xml_children = []

    @classmethod
    def _from_xml(cls, node: etree):
        name = node.get("name", "New Track")
        key_node = node.find("key")
        if key_node is None:
            raise ValueError("Track XML must contain a 'key' element")
        key = PluginKey._from_xml(key_node)
        track = cls(name, key)
        track.__xml_attributes = node.attrib
        for child in node:
            if child.tag != "key":
                track.__xml_children.append(child)
        return track

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
        for key, value in self.__xml_attributes.items():
            node.set(key, value)
        for child in self.__xml_children:
            node.append(child)
        node.set("name", self.__name)
        key_node = etree.SubElement(node, "key")
        self.__key._to_xml(key_node)

    def __str__(self):
        return self.__name + " " + str(self.__key)
