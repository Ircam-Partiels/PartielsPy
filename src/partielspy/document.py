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

    def _to_xml(self, root: etree):
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
