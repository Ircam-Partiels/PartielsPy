"""A class for Reaper export configuration"""

from enum import StrEnum, auto

from .base import ExportConfigBase


class ExportConfigReaper(ExportConfigBase):
    """Reaper export configuration class

    This class is used to configure the export of files in Reaper format.
    it is used in the export method of the :class:`partielspy.partiels` class.

    Args:
        reaper_type (ExportConfigReaper.ReaperTypes): the type of the reaper format\
        (default: REGION)
    """

    class ReaperTypes(StrEnum):
        REGION = auto()
        MARKER = auto()

    def __init__(
        self,
        reaper_type: ReaperTypes = ReaperTypes.REGION,
        adapt_to_sample_rate: bool = False,
    ):
        super().__init__(adapt_to_sample_rate=adapt_to_sample_rate)
        self.reaper_type = reaper_type

    @property
    def reaper_type(self) -> ReaperTypes:
        return self.__reaper_type

    @reaper_type.setter
    def reaper_type(self, value: ReaperTypes):
        self.__reaper_type = ExportConfigReaper.ReaperTypes(value)

    def to_cli_args(self) -> list[str]:
        res = super().to_cli_args()
        res.append("--format=reaper")
        res.append("--reapertype=" + self.reaper_type.value)
        return res
