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

    def _to_xml(self, node: etree):
        node.set("identifier", self.__identifier)
        node.set("feature", self.__feature)

    @classmethod
    def from_json(cls, data: dict):
        if not isinstance(data, dict):
            raise TypeError("Expected a dictionary")
        identifier = data.get("identifier", "")
        feature = data.get("feature", "")
        return cls(identifier=identifier, feature=feature)

    def _to_json(self) -> dict:
        return {
            "identifier": self.__identifier,
            "feature": self.__feature,
        }
