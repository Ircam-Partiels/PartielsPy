"""An abstract class for text export configuration"""

from abc import abstractmethod

from .base import ExportConfigBase


class ExportConfigTextBase(ExportConfigBase):
    """Text export configuration class

    This is the base text class used to configure the export of the document. Is not intended to \
    be used directly but inherited by the ExportConfig classes:
    - :class:`partielspy.export_configs.csv.ExportConfigCsv`
    - :class:`partielspy.export_configs.json.ExportConfigJson`
    - :class:`partielspy.export_configs.cue.ExportConfigCue`

    Args:
        ignore_matrix_tracks (bool): the matrix tracks are ignored (default: False)
    """

    def __init__(
        self, ignore_matrix_tracks: bool = False, adapt_to_sample_rate: bool = False
    ):
        super().__init__(adapt_to_sample_rate=adapt_to_sample_rate)
        self.ignore_matrix_tracks = ignore_matrix_tracks

    @property
    def ignore_matrix_tracks(self) -> bool:
        return self.__ignore_matrix_tracks

    @ignore_matrix_tracks.setter
    def ignore_matrix_tracks(self, value: bool):
        self.__ignore_matrix_tracks = value

    @abstractmethod
    def to_cli_args(self) -> list[str]:
        res = super().to_cli_args()
        if self.ignore_matrix_tracks:
            res.append("--nogrids")
        return res
