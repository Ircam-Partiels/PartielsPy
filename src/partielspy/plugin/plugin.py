from lxml import etree

from .key import PluginKey


class Plugin:
    def __init__(self, key: PluginKey = None):
        if key is None:
            self.__key = PluginKey()
        elif not isinstance(key, PluginKey):
            raise TypeError("key must be an instance of PluginKey")
        else:
            self.__key = key

    @property
    def key(self) -> PluginKey:
        return self.__key

    @classmethod
    def _from_xml(cls, key_node: etree):
        key = PluginKey._from_xml(key_node)
        return cls(key)

    def _to_xml(self, node):
        key_node = etree.SubElement(node, "key")
        self.__key._to_xml(key_node)

    def _to_json(self) -> dict:
        return {"key": self.__key._to_json()}
