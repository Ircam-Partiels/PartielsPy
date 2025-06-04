"""A class for JSON export configuration"""

from .text_base import ExportConfigTextBase


class ExportConfigJson(ExportConfigTextBase):
    """JSON export configuration class

    This class is used to configure the export of files in JSON format.
    It is used in the export method of the :class:`partielspy.partiels` class.

    Args:
        include_plugin_description (bool): the plugin description is included (default: False)
    """

    def __init__(
        self,
        include_plugin_description: bool = False,
        ignore_matrix_tracks: bool = False,
        adapt_to_sample_rate: bool = False,
    ):
        super().__init__(
            ignore_matrix_tracks=ignore_matrix_tracks,
            adapt_to_sample_rate=adapt_to_sample_rate,
        )
        self.include_plugin_description = include_plugin_description

    @property
    def include_plugin_description(self) -> bool:
        return self.__include_plugin_description

    @include_plugin_description.setter
    def include_plugin_description(self, value: bool):
        self.__include_plugin_description = value

    def to_cli_args(self) -> list[str]:
        res = super().to_cli_args()
        res.append("--format=json")
        if self.include_plugin_description:
            res.append("--description")
        return res
