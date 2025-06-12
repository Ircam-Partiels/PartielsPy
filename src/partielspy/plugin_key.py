from lxml import etree


class PluginKey:
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
