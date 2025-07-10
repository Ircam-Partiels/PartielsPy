"""A class for export configuration"""

from enum import StrEnum, auto


class ExportConfig:
    """Export configuration class

    This is the class used to configure the export of the document.

    Args:
        format (ExportConfig.Formats): the export format (default: ``CSV``)
        adapt_to_sample_rate (bool): the block size and the step size of the analyzes \
        are adapted following the sample rate (default: False)
        ignore_matrix_tracks (bool): the matrix tracks are ignored (default: False)
        csv_include_header (bool): the header row is included before the data rows (default: False)
        csv_columns_separator (ExportConfig.CsvColumnSeparators): the separator character between \
        columns (default: COMMA)
        json_include_plugin_description (bool): the plugin description is included\
        (default: False)
        reaper_type (ExportConfig.ReaperTypes): the type of the reaper format\
        (default: ``REGION``)
        image_width (int): the image_width of the image in pixels (default: 1280)
        image_height (int): the image_height of the image in pixels (default: 720)
        image_ppi (int) : the pixel density of the exported image in pixels per inch \
        (default: 72)
        image_group_overlay (bool): the images of groups are exported instead of the\
        images of tracks (default: False)
    """

    class Formats(StrEnum):
        """Enum for the export formats"""

        CSV = auto()
        LAB = auto()
        JSON = auto()
        CUE = auto()
        REAPER = auto()
        JPEG = auto()
        PNG = auto()

    class CsvColumnSeparators(StrEnum):
        """Enum for the CSV column separators"""

        COMMA = auto()
        SPACE = auto()
        TAB = auto()
        PIPE = auto()
        SLASH = auto()
        COLON = auto()

    class ReaperTypes(StrEnum):
        """Enum for the Reaper export types"""

        REGION = auto()
        MARKER = auto()

    def __init__(
        self,
        format: Formats,
        adapt_to_sample_rate: bool = False,
        ignore_matrix_tracks: bool = False,
        csv_include_header: bool = False,
        csv_columns_separator: CsvColumnSeparators = CsvColumnSeparators.COMMA,
        json_include_plugin_description: bool = False,
        reaper_type: ReaperTypes = ReaperTypes.REGION,
        image_width: int = 1280,
        image_height: int = 720,
        image_ppi: int = 72,
        image_group_overlay: bool = False,
    ):
        self.format = format
        self.adapt_to_sample_rate = adapt_to_sample_rate
        self.ignore_matrix_tracks = ignore_matrix_tracks
        self.csv_include_header = csv_include_header
        self.csv_columns_separator = csv_columns_separator
        self.json_include_plugin_description = json_include_plugin_description
        self.reaper_type = reaper_type
        self.image_width = image_width
        self.image_height = image_height
        self.image_ppi = image_ppi
        self.image_group_overlay = image_group_overlay

    @property
    def format(self) -> Formats:
        return self.__format

    @format.setter
    def format(self, value: Formats):
        self.__format = ExportConfig.Formats(value)

    @property
    def adapt_to_sample_rate(self) -> bool:
        return self.__adapt_to_sample_rate

    @adapt_to_sample_rate.setter
    def adapt_to_sample_rate(self, value: bool):
        self.__adapt_to_sample_rate = value

    @property
    def ignore_matrix_tracks(self) -> bool:
        return self.__ignore_matrix_tracks

    @ignore_matrix_tracks.setter
    def ignore_matrix_tracks(self, value: bool):
        self.__ignore_matrix_tracks = value

    @property
    def csv_include_header(self) -> bool:
        return self.__csv_include_header

    @csv_include_header.setter
    def csv_include_header(self, value: bool):
        self.__csv_include_header = value

    @property
    def csv_columns_separator(self) -> CsvColumnSeparators:
        return self.__csv_columns_separator

    @csv_columns_separator.setter
    def csv_columns_separator(self, value: CsvColumnSeparators):
        self.__csv_columns_separator = ExportConfig.CsvColumnSeparators(value)

    @property
    def json_include_plugin_description(self) -> bool:
        return self.__json_include_plugin_description

    @json_include_plugin_description.setter
    def json_include_plugin_description(self, value: bool):
        self.__json_include_plugin_description = value

    @property
    def reaper_type(self) -> ReaperTypes:
        return self.__reaper_type

    @reaper_type.setter
    def reaper_type(self, value: ReaperTypes):
        self.__reaper_type = ExportConfig.ReaperTypes(value)

    @property
    def image_width(self) -> int:
        return self.__image_width

    @image_width.setter
    def image_width(self, image_width: int):
        self.__image_width = image_width

    @property
    def image_height(self) -> int:
        return self.__image_height

    @image_height.setter
    def image_height(self, image_height: int):
        self.__image_height = image_height

    @property
    def image_ppi(self) -> int:
        return self.__image_ppi

    @image_ppi.setter
    def image_ppi(self, value: int):
        self.__image_ppi = value

    @property
    def image_group_overlay(self) -> bool:
        return self.__image_group_overlay

    @image_group_overlay.setter
    def image_group_overlay(self, value: bool):
        self.__image_group_overlay = value

    def to_cli_args(self) -> list[str]:
        res = []
        res.append("--format=" + self.format.value)
        if self.adapt_to_sample_rate:
            res.append("--adapt")
        if (
            self.format == ExportConfig.Formats.JPEG
            or self.format == ExportConfig.Formats.PNG
        ):
            res.append("--width=" + str(self.image_width))
            res.append("--height=" + str(self.image_height))
            res.append("--ppi=" + str(self.image_ppi))
            if self.image_group_overlay:
                res.append("--groups")
        else:
            if self.ignore_matrix_tracks:
                res.append("--nogrids")
            if self.format == ExportConfig.Formats.CSV:
                res.append("--separator=" + self.csv_columns_separator.value)
                if self.csv_include_header:
                    res.append("--header")
            elif self.format == ExportConfig.Formats.REAPER:
                res.append("--reapertype=" + self.reaper_type.value)
            elif self.format == ExportConfig.Formats.JSON:
                if self.json_include_plugin_description:
                    res.append("--description")
        return res
