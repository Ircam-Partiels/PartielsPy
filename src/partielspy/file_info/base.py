import copy
from pathlib import Path

from lxml import etree


class FileInfo:
    def __init__(self, path: Path | str = ""):
        self.__path = str(path)
        self.__xml_node = etree.Element("file")

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, path: Path | str):
        self.__path = str(path)

    def _from_xml(self, node: etree.Element):
        self.path = node.get("path", self.path)
        self.__xml_node = copy.deepcopy(node)

    def _to_xml(self):
        node = copy.deepcopy(self.__xml_node)
        node.set("path", self.__path)
        return node
