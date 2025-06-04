"""A class for cue export configuration"""

from .text_base import ExportConfigTextBase


class ExportConfigCue(ExportConfigTextBase):
    """cue export configuration class

    This class is used to configure the export of files in cue format.
    It is used in the export method of the :class:`partielspy.partiels` class.
    """

    def __init__(
        self,
        ignore_matrix_tracks: bool = False,
        adapt_to_sample_rate: bool = False,
    ):
        super().__init__(
            ignore_matrix_tracks=ignore_matrix_tracks,
            adapt_to_sample_rate=adapt_to_sample_rate,
        )

    def to_cli_args(self) -> list[str]:
        res = super().to_cli_args()
        res.append("--format=cue")
        return res
