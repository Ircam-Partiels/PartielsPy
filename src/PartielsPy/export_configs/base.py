"""An abstract class for export configuration"""

from abc import ABC, abstractmethod


class ExportConfigBase(ABC):
    """Base export configuration class

    This is the base class used to configure the export of the document. Is not intended to \
    be used directly but inherited by the ExportConfig classes:
    - :class:`PartielsPy.export_configs.image`
    - :class:`PartielsPy.export_configs.lab`
    - :class:`PartielsPy.export_configs.reaper`
    - :class:`PartielsPy.export_configs.text_base`

    Args:
        adapt_to_sample_rate (bool): the block size and the step size of the analyzes \
        are adapted following the sample rate (default: False)
    """

    def __init__(self, adapt_to_sample_rate: bool = False):
        self.__adapt_to_sample_rate = adapt_to_sample_rate

    @property
    def adapt_to_sample_rate(self) -> bool:
        return self.__adapt_to_sample_rate

    @adapt_to_sample_rate.setter
    def adapt_to_sample_rate(self, value: bool):
        self.__adapt_to_sample_rate = value

    @abstractmethod
    def to_cli_args(self) -> list[str]:
        if self.adapt_to_sample_rate:
            return ["--adapt"]
        return []
