"""A class for audio file layout"""

from pathlib import Path

from lxml import etree


class AudioFileChannel:
    """This class represents an audio file channel and its\
    associated channel number.
    """

    def __init__(self, file: Path | str, channel: int = 0):
        self.file = file
        self.channel = channel

    @property
    def file(self) -> str:
        return self.__file

    @file.setter
    def file(self, file: Path | str):
        if not isinstance(file, (Path, str)):
            raise TypeError("File must be a Path or a string.")
        self.__file = str(file)

    @property
    def channel(self) -> int:
        return self.__channel

    @channel.setter
    def channel(self, channel: int):
        if not isinstance(channel, int) or channel < 0:
            raise ValueError("Channel must be a non-negative integer.")
        self.__channel = channel

    def _from_xml(self, node: etree.Element):
        self.file = node.get("file", self.file)
        self.channel = int(node.get("channel", self.channel))

    def _to_xml(self) -> etree.Element:
        node = etree.Element("value")
        node.set("file", self.file)
        node.set("channel", str(self.channel))
        return node


class AudioFileLayout(list[AudioFileChannel]):
    """This class represents the audio file layout of a document."""

    def _from_xml(self, nodes: list[etree.Element]):
        self.clear()
        for node in nodes:
            afc = AudioFileChannel("")
            afc._from_xml(node)
            self.append(afc)

    def _to_xml(self) -> list[etree.Element]:
        all_nodes = []
        for channel in self:
            all_nodes.append(channel._to_xml())
        return all_nodes
