"""A class for Lab export configuration"""

from .base import ExportConfigBase


class ExportConfigLab(ExportConfigBase):
    """Lab export configuration class

    This class is used to configure the export of files in Lab format.
    It is used in the export method of the :class:`PartielsPy.partiels` class.
    """

    def __init__(self, adapt_to_sample_rate: bool = False):
        super().__init__(adapt_to_sample_rate=adapt_to_sample_rate)

    def to_cli_args(self) -> list[str]:
        res = super().to_cli_args()
        res.append("--format=lab")
        return res
