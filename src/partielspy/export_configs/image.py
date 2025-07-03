"""A class for image export configuration"""

from enum import StrEnum, auto

from .base import ExportConfigBase


class ExportConfigImage(ExportConfigBase):
    """Image export configuration class

    This class is used to configure the export of files in image formats.
    It is used in the export method of the :class:`Partiels <partielspy.partiels>` class.

    Args:
        format (Formats): the format of the image (default: Formats.JPEG)
        width (int): the width of the image in pixels (default: 1280)
        height (int): the height of the image in pixels (default: 720)
        group_overlay (bool): the images of groups are exported instead of the images of tracks \
        (default: False)
    """

    class Formats(StrEnum):
        """Enum for the image format"""

        JPEG = auto()
        PNG = auto()

    def __init__(
        self,
        format: Formats = Formats.JPEG,
        width: int = 1280,
        height: int = 720,
        group_overlay: bool = False,
        adapt_to_sample_rate: bool = False,
    ):
        super().__init__(adapt_to_sample_rate=adapt_to_sample_rate)
        self.format = format
        self.width = width
        self.height = height
        self.group_overlay = group_overlay

    @property
    def format(self) -> Formats:
        return self.__format

    @format.setter
    def format(self, format: Formats):
        self.__format = ExportConfigImage.Formats(format)

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, width: int):
        self.__width = width

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int):
        self.__height = height

    @property
    def group_overlay(self) -> bool:
        return self.__group_overlay

    @group_overlay.setter
    def group_overlay(self, value: bool):
        self.__group_overlay = value

    def to_cli_args(self) -> list[str]:
        res = super().to_cli_args()
        res += [
            "--format=" + self.format.value,
            "--width=" + str(self.width),
            "--height=" + str(self.height),
        ]
        if self.__group_overlay:
            res.append("--groups")
        return res
