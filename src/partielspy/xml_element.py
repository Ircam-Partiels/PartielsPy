from abc import ABC, abstractmethod

from lxml import etree


class XmlElement(ABC):
    def __init__(
        self, ignored_attributes: list[str] = [], ignored_children: list[str] = []
    ):
        self.__ignored_attributes = ignored_attributes
        self.__ignored_children = ignored_children
        self.__attributes = {}
        self.__children = []

    @abstractmethod
    def _from_xml(self, node: etree):
        pass

    def from_xml(self, node: etree):
        for attr in node.attrib:
            if attr not in self.__ignored_attributes:
                self.__attributes[attr] = node.attrib[attr]
        for child in node:
            if child.tag not in self.__ignored_children:
                self.__children.append(child)

    def to_xml(self, node: etree):
        for key, value in self.__attributes.items():
            node.set(key, value)
        for child in self.__children:
            node.append(child)
