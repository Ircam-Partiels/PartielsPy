from lxml import etree


class Track:
    def __init__(self, name: str = "New Track"):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    def _to_xml(self, node: etree):
        node.set("name", self.__name)

    def __str__(self):
        return self.__name
