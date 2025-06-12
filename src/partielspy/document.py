import uuid

from lxml import etree

from .group import Group


class Document:
    def __init__(self):
        self.__groups = {}

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

    def _to_xml(self, node: etree):
        for group_identifier, group in self.__groups.items():
            layout_node = etree.Element("layout")
            layout_node.set("value", group_identifier)
            node.append(layout_node)
            group_node = etree.Element("groups")
            group_node.set("identifier", group_identifier)
            group._to_xml(group_node)
            node.append(group_node)

    def __str__(self):
        res = ""
        for group in self.groups:
            res += group.__str__()
            res += "\n" if group != self.groups[-1] else ""
        return res
