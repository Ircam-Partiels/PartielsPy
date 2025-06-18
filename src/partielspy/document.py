import copy
import uuid
from pathlib import Path
from typing import Any

from lxml import etree

from .group import Group
from .version import Version


class Document:
    def __init__(self):
        self.__xml_node = etree.Element("document")
        self.__groups = {}

    @property
    def groups(self) -> list[Group]:
        return list(self.__groups.values())

    def add_group(self, group: Group):
        if not isinstance(group, Group):
            raise TypeError("Expected a Group instance")
        if group in self.groups:
            raise ValueError("Group already exists in document")
        self.__groups[uuid.uuid4().hex] = group

    def remove_group(self, group: Group):
        for key, value in self.__groups.items():
            if value == group:
                del self.__groups[key]
                return
        raise ValueError("Group not found in document")

    def _from_xml(self, root: etree):
        group_layouts = root.findall("layout")
        for group_layout in group_layouts:
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
        tree = etree.parse(file)
        root = tree.getroot()
        if root.tag != "document":
            raise ValueError("Invalid XML document: root tag must be 'document'")
        document = cls()
        document._from_xml(root)
        return document

    def _to_xml(self) -> etree.Element:
        root = copy.deepcopy(self.__xml_node)
        root.set("MiscModelVersion", Version.get_compatibility_version_int())
        for group_identifier, group in self.__groups.items():
            layout = etree.Element("layout")
            layout.set("value", group_identifier)
            root.append(layout)
            root.extend(group._to_xml(group_identifier))
        return root

    def save(self, file: str | Path):
        root = self._to_xml()
        xml = etree.ElementTree(root)
        xml.write(file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
