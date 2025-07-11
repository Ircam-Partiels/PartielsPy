"""PartielsPy - Document Module"""

import copy
import uuid
from pathlib import Path
from typing import Any

from lxml import etree

from .audio_file_layout import AudioFileChannel, AudioFileLayout
from .group import Group
from .version import Version


class Document:
    """This class represents a document in PartielsPy.

    It contains an :class:`AudioFileLayout <partielspy.audio_file_layout>`\
    that describes the audio file layout of the document, and a collection \
    of :class:`Group <partielspy.group>`, each of which can contain \
    multiple :class:`Track <partielspy.track>`. The document can be loaded \
    from and saved to an ptldoc file.

    Args:
        document_file (str | Path, optional): The path to the ptldoc file to load.
            If not provided, an empty document is created.
        audio_file_layout (AudioFileLayout | str | Path | AudioFileChannel, optional):
            The audio file layout for the document. This can be an instance of \
            :class:`AudioFileLayout <partielspy.audio_file_layout>`, a string or
            a Path to an audio file, or an instance of \
            :class:`AudioFileChannel <partielspy.audio_file_layout>`.
            If not provided, an empty audio file layout is created.
    """

    def __init__(
        self,
        document_file: str | Path = None,
        audio_file_layout: AudioFileLayout | str | Path | AudioFileChannel = None,
    ):
        self.__xml_node = etree.Element("document")
        self.__groups = {}
        self.audio_file_layout = AudioFileLayout()
        if document_file is not None:
            self._from_xml(etree.parse(document_file).getroot())
        if audio_file_layout is not None:
            self.audio_file_layout = audio_file_layout

    @property
    def audio_file_layout(self) -> AudioFileLayout:
        return self.__audio_file_layout

    @audio_file_layout.setter
    def audio_file_layout(self, value: AudioFileLayout | AudioFileChannel | str | Path):
        if isinstance(value, AudioFileLayout):
            self.__audio_file_layout = value
        elif isinstance(value, AudioFileChannel):
            self.__audio_file_layout = AudioFileLayout([value])
        elif isinstance(value, (str | Path)):
            self.__audio_file_layout = AudioFileLayout([AudioFileChannel(file=value)])
        else:
            raise TypeError(
                "Expected an AudioFileLayout, AudioFileChannel, str, or Path instance"
            )

    @property
    def groups(self) -> list[Group]:
        return list(self.__groups.values())

    def add_group(self, group: Group):
        """Add a group to the document.

        This method checks if the group is an instance of :class:`Group <partielspy.group>` \
        and if it already exists in the document.
        If the group is valid and not already present, it adds the group to the document's groups.

        Args:
            group(:class:`Group <partielspy.group>`): The group to add to the document.
        Raises:
            TypeError: If the group is not an instance of :class:`Group <partielspy.group>`.
            ValueError: If the group already exists in the document.
        """
        if not isinstance(group, Group):
            raise TypeError("Expected a Group instance")
        if group in self.groups:
            raise ValueError("Group already exists in document")
        self.__groups[uuid.uuid4().hex] = group

    def remove_group(self, group: Group):
        """Remove a group from the document.

        This method searches for the group in the document's groups and removes it if found.

        Args:
            group(:class:`Group <partielspy.group>`): The group to remove from the document.
        Raises:
            ValueError: If the group is not found in the document.
        """
        for key, value in self.__groups.items():
            if value == group:
                del self.__groups[key]
                return
        raise ValueError("Group not found in document")

    def _from_xml(self, root: etree):
        if root.tag != "document":
            raise ValueError("Invalid document: root tag must be 'document'")
        audio_file_layout = []
        for reader_node in root.findall("reader"):
            value_elem = reader_node.find("value")
            audio_file_layout.append(value_elem)
            root.remove(reader_node)
        self.audio_file_layout._from_xml(audio_file_layout)
        for group_layout in root.findall("layout"):
            layout_value = group_layout.get("value")
            group_node = root.find(f"./groups[@identifier='{layout_value}']")
            group = Group()
            group._from_xml(group_node)
            self.__groups[layout_value] = group
            root.remove(group_layout)
            root.remove(group_node)
        self.__xml_node = copy.deepcopy(root)

    @classmethod
    def load(cls, file: Any):
        """Load a document from an ptldoc file.

        Args:
            file (Any): The file to load.
        Returns:
            Document: An instance of the Document class populated with data from \
            the ptldoc file.
        Raises:
            ValueError: If the document is invalid (does not have the correct \
            root 'document' tag).
        """
        tree = etree.parse(file)
        document = cls()
        document._from_xml(tree.getroot())
        return document

    def _to_xml(self) -> etree.Element:
        root = copy.deepcopy(self.__xml_node)
        root.set("MiscModelVersion", str(Version.get_compatibility_version_int()))
        reader_nodes = self.audio_file_layout._to_xml()
        for reader_node in reader_nodes:
            reader = etree.Element("reader")
            reader.append(reader_node)
            root.append(reader)
        for group_identifier, group in self.__groups.items():
            layout = etree.Element("layout")
            layout.set("value", group_identifier)
            root.append(layout)
            root.extend(group._to_xml(group_identifier))
        return root

    def save(self, file: str | Path):
        """Save the document to an ptldoc file.

        Args:
            file (str | Path): The path to the file where the document will be saved.
        """
        root = self._to_xml()
        xml = etree.ElementTree(root)
        xml.write(file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
