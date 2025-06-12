import uuid
from pathlib import Path

from lxml import etree

from .group import Group
from .track import Track


class Document:
    def __init__(self, path: str | Path = None):
        self.__groups = {}
        self.__xml_attributes = {}
        self.__xml_children = []
        if path:
            self._from_xml(path)

    def _from_xml(self, path: str | Path):
        if not isinstance(path, (str, Path)):
            raise TypeError("Path must be a string or Path object")
        with open(path, "rb") as file:
            xml_content = file.read()
        root = etree.fromstring(xml_content)
        if root.tag != "document":
            raise ValueError("Invalid XML document: root tag must be 'document'")
        self.__xml_attributes = root.attrib
        for child in root:
            if (
                child.tag != "layout"
                and child.tag != "groups"
                and child.tag != "tracks"
            ):
                self.__xml_children.append(child)
        for group_layout in root.findall("layout"):
            layout_value = group_layout.get("value")
            group_node = root.find(f"./groups[@identifier='{layout_value}']")
            group = Group._from_xml(group_node)
            for track_layout in group_node.findall("layout"):
                track_layout_value = track_layout.get("value")
                track_node = root.find(f"./tracks[@identifier='{track_layout_value}']")
                group._tracks_items[track_layout_value] = Track._from_xml(track_node)
            self.__groups[layout_value] = group

    @property
    def groups(self) -> list[Group]:
        return list(self.__groups.values())

    def add_group(self, group: Group):
        if not isinstance(group, Group):
            raise TypeError("Expected a Group instance")
        self.__groups[uuid.uuid4().hex] = group

    def remove_group(self, group: Group):
        for key, value in self.__groups.items():
            if value == group:
                del self.__groups[key]
                return
        raise ValueError("Group not found in document")

    def _to_xml(self, root: etree):
        root.tag = "document"
        for key, value in self.__xml_attributes.items():
            root.set(key, value)
        for child in self.__xml_children:
            root.append(child)

        def element_to_xml(
            parent_node: etree, identifier: str, element: object, tag: str
        ):
            layout = etree.Element("layout")
            layout.set("value", identifier)
            parent_node.append(layout)
            element_node = etree.Element(tag)
            element_node.set("identifier", identifier)
            element._to_xml(element_node)
            root.append(element_node)
            return element_node

        for group_identifier, group in self.__groups.items():
            group_node = element_to_xml(root, group_identifier, group, "groups")
            for track_identifier, track in group._tracks_items.items():
                element_to_xml(group_node, track_identifier, track, "tracks")

    def __str__(self):
        res = ""
        for group in self.groups:
            res += group.__str__()
            res += "\n" if group != self.groups[-1] else ""
        return res
