"""A class for tracks file information"""

import copy
from pathlib import Path

from lxml import etree


class FileInfo:
    """This class represents file information in a track.

    It contains the path to the file used by the track for the export.
    If the path is left to an empty string (""), the track will use its plugin_key instead.
    This class is inherited by the classes:
    - :class:`FileInfoCsv <partielspy.file_info.csv>`
    - :class:`FileInfoLab <partielspy.file_info.lab>`
    If the file is in a CSV format, use the :class:`FileInfoCsv <partielspy.file_info.csv>` class.
    If the file is in a Lab format, use the :class:`FileInfoLab <partielspy.file_info.lab>` class.

    Args:
        path (Path | str): The path to the file associated with the track (default: "")
    """

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

    def _to_xml(self) -> etree.Element:
        node = copy.deepcopy(self.__xml_node)
        node.set("path", self.__path)
        return node
