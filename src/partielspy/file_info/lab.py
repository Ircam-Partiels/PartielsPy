"""A class for tracks LAB file information"""

from .csv import FileInfoCsv


class FileInfoLab(FileInfoCsv):
    """This class represents LAB file information in a track.
    It contains the path to the LAB file used by the track for the export.

    Args:
        path (str): The path to the LAB file associated with the track (default: "")
        columns_separator \
        (:class:`FileInfoCsv.Separators <partielspy.file_info.csv.FileInfoCsv.Separators>`): \
        The separator used in the LAB file (default: ``TAB``)
        use_end_time (bool): Whether to use the end time in the LAB file (default: True)
    """

    def __init__(
        self,
        path: str = "",
        columns_separator: FileInfoCsv.Separators = FileInfoCsv.Separators.TAB,
        use_end_time: bool = True,
    ):
        super().__init__(path, columns_separator, use_end_time)
