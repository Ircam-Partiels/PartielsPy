import uuid

from lxml import etree

from .group import Group
from .version import Version


class Document:
    def __init__(self):
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

    def _to_xml(self, root: etree):
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

    def __str__(self):
        res = "Document:\n"
        for group in self.groups:
            res += group.__str__()
            res += "\n" if group != self.groups[-1] else ""
        return res
