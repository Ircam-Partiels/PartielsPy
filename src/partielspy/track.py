"""PartielsPy - Track Module"""

import copy

from lxml import etree

from .file_info.base import FileInfo
from .file_info.csv import FileInfoCsv
from .file_info.lab import FileInfoLab
from .plugin_key import PluginKey
from .version import Version


class Track:
    """This class represents a track in PartielsPy.

    A track contains a :class:`PluginKey <partielspy.plugin_key>` and a \
    :class:`FileInfo <partielspy.file_info.base>`, along with a name.
    If the file_info is set (with a non-empty path) the plugin_key will be ignored for the export.

    Args:
        name (str): The name of the track (default: "New Track")
        plugin_key (:class:`PluginKey <partielspy.plugin_key>`): The plugin key associated with \
        the track (default: a new empty :class:`PluginKey <partielspy.plugin_key>` instance)
        file_info (:class:`FileInfo <partielspy.file_info.base>`): The file associated with \
        the track (default: a new empty :class:`FileInfo <partielspy.file_info.base>` instance).
    """

    def __init__(self, name: str = "New Track"):
        self.__xml_node = etree.Element("tracks")
        self.__name = name
        self.__plugin_key = PluginKey()
        self.__file_info = FileInfo()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def plugin_key(self) -> PluginKey:
        return self.__plugin_key

    @plugin_key.setter
    def plugin_key(self, value: PluginKey):
        if not isinstance(value, PluginKey):
            raise TypeError("plugin_key must be an instance of PluginKey")
        self.__plugin_key = value

    @property
    def file_info(self) -> FileInfo:
        return self.__file_info

    @file_info.setter
    def file_info(self, value: FileInfo):
        if not isinstance(value, FileInfo):
            raise TypeError("file_info must be an instance of FileInfo")
        self.__file_info = value

    def _from_xml(self, node: etree.Element):
        self.name = node.get("name", self.name)
        plugin_key_node = node.find("key")
        if plugin_key_node is not None:
            self.plugin_key._from_xml(plugin_key_node)
            node.remove(plugin_key_node)
        file_node = node.find("file")
        if file_node is not None:
            if file_node.get("path", "").endswith((".csv")):
                self.file_info = FileInfoCsv()
            if file_node.get("path", "").endswith((".lab")):
                self.file_info = FileInfoLab()
            self.file_info._from_xml(file_node)
            node.remove(file_node)
        self.__xml_node = copy.deepcopy(node)

    def _to_xml(self, identifier: str) -> etree.Element:
        node = copy.deepcopy(self.__xml_node)
        node.set("MiscModelVersion", Version.get_compatibility_version_int())
        node.set("name", self.__name)
        node.set("identifier", identifier)
        node.append(self.__plugin_key._to_xml())
        node.append(self.__file_info._to_xml())
        return node
