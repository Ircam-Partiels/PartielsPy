"""A class for CSV export configuration"""

from enum import StrEnum, auto

from .text_base import ExportConfigTextBase


class ExportConfigCsv(ExportConfigTextBase):
    """CSV export configuration class

    This class is used to configure the export of files in CSV format.
    It is used in the export method of the :class:`partielspy.partiels` class.

    Args:
        include_header (bool): the header row is included before the data rows (default: False)
        columns_separator (ExportConfigCsv.Separators): the separator character between \
        columns (default: COMMA)
    """

    class Separators(StrEnum):
        """Enum for the columns separator"""

        COMMA = auto()
        SPACE = auto()
        TAB = auto()
        PIPE = auto()
        SLASH = auto()
        COLON = auto()

    def __init__(
        self,
        include_header: bool = False,
        columns_separator: Separators = Separators.COMMA,
        ignore_matrix_tracks: bool = False,
        adapt_to_sample_rate: bool = False,
    ):
        super().__init__(
            ignore_matrix_tracks=ignore_matrix_tracks,
            adapt_to_sample_rate=adapt_to_sample_rate,
        )
        self.include_header = include_header
        self.columns_separator = columns_separator

    @property
    def include_header(self) -> bool:
        return self.__include_header

    @include_header.setter
    def include_header(self, value: bool):
        self.__include_header = value

    @property
    def columns_separator(self) -> Separators:
        return self.__columns_separator

    @columns_separator.setter
    def columns_separator(self, value: Separators):
        self.__columns_separator = ExportConfigCsv.Separators(value)

    def to_cli_args(self) -> list[str]:
        res = super().to_cli_args()
        res.append("--format=csv")
        res.append("--separator=" + self.columns_separator.value)
        if self.include_header:
            res.append("--header")
        return res
