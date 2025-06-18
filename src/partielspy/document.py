import uuid
from pathlib import Path

from lxml import etree

from .group import Group
from .version import Version
from .xml_element import XmlElement


class Document(XmlElement):
    __ignored_children = ["layout", "groups", "tracks"]

    def __init__(self):
        self.__groups = {}
        super().__init__(ignored_children=Document.__ignored_children)

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
        self.from_xml(root)
        for group_layout in root.findall("layout"):
            layout_value = group_layout.get("value")
            group_node = root.find(f"./groups[@identifier='{layout_value}']")
            self.__groups[layout_value] = Group._from_xml(group_node)

    @classmethod
    def load(cls, file: bytes) -> "Document":
        root = etree.fromstring(file)
        if root.tag != "document":
            raise ValueError("Invalid XML document: root tag must be 'document'")
        document = cls()
        document._from_xml(root)
        return document

    def to_xml(self, root: etree):
        super().to_xml(root)
        root.set("MiscModelVersion", Version.get_compatibility_version_int())
        for group_identifier, group in self.__groups.items():
            layout = etree.Element("layout")
            root.append(layout)
            layout.set("value", group_identifier)
            group_node = etree.Element("groups")
            root.append(group_node)
            group_node.set("identifier", group_identifier)
            group_node.set("MiscModelVersion", Version.get_compatibility_version_int())
            group._to_xml(group_node)

    def save(self, file: str | Path):
        root = etree.Element("document")
        self.to_xml(root)
        xml = etree.ElementTree(root)
        xml.write(file, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    def to_json(self) -> dict:
        res = []
        for group in self.groups:
            res.append(group._to_json())
        return res
