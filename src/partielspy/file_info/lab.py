from .csv import FileInfoCsv


class FileInfoLab(FileInfoCsv):
    def __init__(
        self,
        path: str = "",
        columns_separator: FileInfoCsv.Separators = FileInfoCsv.Separators.TAB,
        use_end_time: bool = True,
    ):
        super().__init__(path, columns_separator, use_end_time)
