from enum import StrEnum
from pathlib import Path

from lxml import etree

from .base import FileInfo


class FileInfoCsv(FileInfo):
    class Separators(StrEnum):
        """Enum for the columns separator"""

        COMMA = ","
        SPACE = " "
        TAB = "\t"
        PIPE = "|"
        SLASH = "/"
        COLON = ":"

    def __init__(
        self,
        path: Path | str = "",
        columns_separator: Separators = Separators.COMMA,
        use_end_time: bool = False,
    ):
        super().__init__(path)
        self.__columns_separator = columns_separator
        self.__use_end_time = use_end_time

    @property
    def columns_separator(self) -> Separators:
        return self.__columns_separator

    @columns_separator.setter
    def columns_separator(self, value: Separators):
        self.__columns_separator = FileInfoCsv.Separators(value)

    @property
    def use_end_time(self) -> bool:
        return self.__use_end_time

    @use_end_time.setter
    def use_end_time(self, use_end_time: bool):
        self.__use_end_time = use_end_time

    def _from_xml(self, node: etree.Element):
        args_node = node.find("args")
        if args_node is not None:
            pairs = {
                pair.get("key"): pair.get("value") for pair in args_node.findall("pair")
            }
            separator = pairs.get("separator", self.columns_separator.value)
            if separator in FileInfoCsv.Separators._value2member_map_:
                self.columns_separator = FileInfoCsv.Separators(separator)
            else:
                raise ValueError(f"Invalid separator: {separator}")
            self.use_end_time = pairs.get("useendtime", "") == "true"
            node.remove(args_node)
        super()._from_xml(node)

    def _to_xml(self):
        node = super()._to_xml()
        args_node = etree.Element("args")
        args_node.append(
            etree.Element("pair", key="separator", value=self.columns_separator.value)
        )
        args_node.append(
            etree.Element(
                "pair", key="useendtime", value=str(self.use_end_time).lower()
            )
        )
        node.append(args_node)
        return node
