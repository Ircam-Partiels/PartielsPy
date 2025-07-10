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
    The csv_columns_separator and csv_use_end_time arguments should only be used for CSV files.

    Args:
        path (Path | str): The path to the file associated with the track (default: "")
        csv_columns_separator (FileInfo.CsvColumnSeparators): The separator used in the CSV file
            (default: ``COMMA``)
        csv_use_end_time (bool): Whether to use the end time in the CSV file (default: False)
     Raises:
            ValueError: If the file is not empty and doesn't exist.
            TypeError: If the file extension is not supported.
            TypeError: If the csv_columns_separator or csv_use_end_time is set for non-CSV files
    """

    class CsvColumnSeparators(StrEnum):
        """Enum for the CSV column separators"""

        COMMA = ","
        SPACE = " "
        TAB = "\t"
        PIPE = "|"
        SLASH = "/"
        COLON = ":"

    def __init__(
        self,
        path: Path | str = "",
        csv_columns_separator: CsvColumnSeparators = None,
        csv_use_end_time: bool = None,
    ):
        self.__set_and_validate_member_values(
            path=path,
            csv_columns_separator=csv_columns_separator,
            csv_use_end_time=csv_use_end_time,
        )
        self.__xml_node = etree.Element("file")

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: Path | str):
        self.__set_and_validate_member_values(
            path=value,
            csv_columns_separator=self.__csv_columns_separator,
            csv_use_end_time=self.__csv_use_end_time,
        )

    @property
    def csv_columns_separator(self) -> CsvColumnSeparators:
        return self.__csv_columns_separator

    @csv_columns_separator.setter
    def csv_columns_separator(self, csv_columns_separator: CsvColumnSeparators):
        self.__set_and_validate_member_values(
            path=self.__path,
            csv_columns_separator=csv_columns_separator,
            csv_use_end_time=self.__csv_use_end_time,
        )

    @property
    def csv_use_end_time(self) -> bool:
        return self.__csv_use_end_time

    @csv_use_end_time.setter
    def csv_use_end_time(self, csv_use_end_time: bool):
        self.__set_and_validate_member_values(
            path=self.__path,
            csv_columns_separator=self.__csv_columns_separator,
            csv_use_end_time=csv_use_end_time,
        )

    def _from_xml(self, node: etree.Element):
        self.__path = node.get("path", self.path)
        args_node = node.find("args")
        if args_node is not None:
            pairs = {
                pair.get("key"): pair.get("value") for pair in args_node.findall("pair")
            }
            if "separator" in pairs:
                self.__csv_columns_separator = FileInfo.CsvColumnSeparators(
                    pairs.get("separator")
                )
            if "useendtime" in pairs:
                self.__csv_use_end_time = pairs.get("useendtime") == "true"
            node.remove(args_node)
        self.__xml_node = copy.deepcopy(node)

    def _to_xml(self) -> etree.Element:
        node = copy.deepcopy(self.__xml_node)
        node.set("path", self.__path)
        args_node = etree.Element("args")
        if self.__csv_columns_separator is not None:
            args_node.append(
                etree.Element(
                    "pair", key="separator", value=self.__csv_columns_separator.value
                )
            )
        if self.__csv_use_end_time is not None:
            args_node.append(
                etree.Element(
                    "pair", key="useendtime", value=str(self.__csv_use_end_time).lower()
                )
            )
        if len(args_node) > 0:
            node.append(args_node)
        return node

    def __set_and_validate_member_values(
        self,
        path: Path | str = "",
        csv_columns_separator: CsvColumnSeparators = None,
        csv_use_end_time: bool = None,
    ):
        """Set the member and validate the file information."""
        path = str(path)
        if path != "":
            if not Path(path).is_file():
                raise ValueError(f"The path {path} not a file.")
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
            if csv_columns_separator is None:
                self.__csv_columns_separator = FileInfo.CsvColumnSeparators.COMMA
            elif isinstance(csv_columns_separator, FileInfo.CsvColumnSeparators):
                self.__csv_columns_separator = csv_columns_separator
            else:
                raise TypeError(
                    f"The csv_columns_separator must be an instance of \
                        '{FileInfo.CsvColumnSeparators}', got '{csv_columns_separator}'"
                )
            self.__csv_use_end_time = (
                csv_use_end_time if csv_use_end_time is not None else False
            )
        elif self.path.endswith(".lab"):
            if (
                csv_columns_separator is not None
                and csv_columns_separator != FileInfo.CsvColumnSeparators.TAB
            ):
                raise ValueError(
                    f"The csv_columns_separator must be '{FileInfo.CsvColumnSeparators.TAB}' \
                        for LAB files, got '{csv_columns_separator}'"
                )
            if csv_use_end_time is not None and not csv_use_end_time:
                raise ValueError(
                    f"The csv_use_end_time must be 'True' for LAB files, got '{csv_use_end_time}'"
                )
            self.__csv_columns_separator = FileInfo.CsvColumnSeparators.TAB
            self.__csv_use_end_time = True
        else:
            if csv_columns_separator is not None:
                raise TypeError("The csv_columns_separator is only used for CSV files")
            if csv_use_end_time is not None:
                raise TypeError("The csv_use_end_time is only used for CSV files")
            self.__csv_columns_separator = None
            self.__csv_use_end_time = None
