from lxml import etree


class PluginKey:
    def __init__(self, identifier: str = "", feature: str = ""):
        self.__identifier = identifier
        self.__feature = feature

    @classmethod
    def _from_xml(cls, node: etree):
        identifier = node.get("identifier", "")
        feature = node.get("feature", "")
        return cls(identifier, feature)

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def feature(self) -> str:
        return self.__feature

    def _to_xml(self, node: etree):
        node.set("identifier", self.__identifier)
        node.set("feature", self.__feature)

    def __str__(self):
        return self.__identifier + " " + self.__feature
