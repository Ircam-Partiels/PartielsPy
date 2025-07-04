"""A class for tracks file information"""

import copy
from enum import StrEnum
from pathlib import Path

from lxml import etree


class FileInfo:
    """This class represents file information in a track.

    It contains the path to the file used by the track for the export and parsing information for \
    the CSV format.
    The supported file formats are JSON, CSV, LAB and CUE (with the extension .json, .csv, .lab \
    and .cue).
    If the file path is defined, the track will use file instead of performing the analysis
    on the audio data.
    The columns_separator and use_end_time arguments shoud only be used for CSV files.

    Args:
        path (Path | str): The path to the file associated with the track (default: "")
        columns_separator (FileInfo.Separators): The separator used in the CSV file
            (default: ``COMMA``)
        use_end_time (bool): Whether to use the end time in the CSV file (default: False)
     Raises:
            ValueError: If the file is not empty and doesn't exist.
            TypeError: If the file extension is not supported.
            TypeError: If the columns_separator or use_end_time is set for non-CSV files
    """

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
        columns_separator: Separators = None,
        use_end_time: bool = None,
    ):
        self.__set_validate(
            path=path, columns_separator=columns_separator, use_end_time=use_end_time
        )
        self.__xml_node = etree.Element("file")

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: Path | str):
        self.__set_validate(
            path=value,
            columns_separator=self.__columns_separator,
            use_end_time=self.__use_end_time,
        )

    @property
    def columns_separator(self) -> Separators:
        return self.__columns_separator

    @columns_separator.setter
    def columns_separator(self, columns_separator: Separators):
        self.__set_validate(
            path=self.__path,
            columns_separator=columns_separator,
            use_end_time=self.__use_end_time,
        )

    @property
    def use_end_time(self) -> bool:
        return self.__use_end_time

    @use_end_time.setter
    def use_end_time(self, use_end_time: bool):
        self.__set_validate(
            path=self.__path,
            columns_separator=self.__columns_separator,
            use_end_time=use_end_time,
        )

    def _from_xml(self, node: etree.Element):
        self.__path = node.get("path", self.path)
        args_node = node.find("args")
        if args_node is not None:
            pairs = {
                pair.get("key"): pair.get("value") for pair in args_node.findall("pair")
            }
            if "separator" in pairs:
                self.__columns_separator = FileInfo.Separators(pairs.get("separator"))
            if "useendtime" in pairs:
                self.__use_end_time = pairs.get("useendtime") == "true"
            node.remove(args_node)
        self.__xml_node = copy.deepcopy(node)

    def _to_xml(self) -> etree.Element:
        node = copy.deepcopy(self.__xml_node)
        node.set("path", self.__path)
        args_node = etree.Element("args")
        if self.__columns_separator is not None:
            args_node.append(
                etree.Element(
                    "pair", key="separator", value=self.__columns_separator.value
                )
            )
        if self.__use_end_time is not None:
            args_node.append(
                etree.Element(
                    "pair", key="useendtime", value=str(self.__use_end_time).lower()
                )
            )
        if len(args_node) > 0:
            node.append(args_node)
        return node

    def __set_validate(
        self,
        path: Path | str = "",
        columns_separator: Separators = None,
        use_end_time: bool = None,
    ):
        """Set the member and Validate the file information."""
        path = str(path)
        if path != "":
            if not Path(path).is_file() and not Path(path).exists():
                raise ValueError(f"The path {path} not an existing file.")
            if (
                not path.endswith(".json")
                and not path.endswith(".csv")
                and not path.endswith(".lab")
                and not path.endswith(".cue")
            ):
                raise TypeError(
                    f"The file extension of {path} is not supported. "
                    "Supported extensions are: .json, .csv, .lab, .cue"
                )
        self.__path = path
        if self.path.endswith(".csv"):
            # Set the columns separator (use COMMA by default)
            if columns_separator is None:
                self.__columns_separator = FileInfo.Separators.COMMA
            elif isinstance(columns_separator, FileInfo.Separators):
                self.__columns_separator = columns_separator
            else:
                raise TypeError(
                    f"The columns_separator must be an instance of FileInfo.Separators, \
                        got '{columns_separator}'"
                )
            self.__use_end_time = use_end_time if use_end_time is not None else False
        elif self.path.endswith(".lab"):
            if (
                columns_separator is not None
                and columns_separator != FileInfo.Separators.TAB
            ):
                raise ValueError(
                    f"The column_separator must be '{FileInfo.Separators.TAB}' for LAB files, \
                        got '{columns_separator}'"
                )
            if use_end_time is not None and not use_end_time:
                raise ValueError(
                    f"The use_end_time must be 'True' for LAB files, got '{use_end_time}'"
                )
            self.__columns_separator = FileInfo.Separators.TAB
            self.__use_end_time = True
        else:
            if columns_separator is not None:
                raise TypeError("The column_separator is only used for CSV files")
            if use_end_time is not None:
                raise TypeError("The use_end_time is only used for CSV files")
            self.__columns_separator = None
            self.__use_end_time = None
