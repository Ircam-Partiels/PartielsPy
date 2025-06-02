from pathlib import Path

from lxml import etree

from .group import Group


class Document:
    @classmethod
    def from_ptldoc(cls, filepath: str | Path):
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.is_file():
            raise FileNotFoundError(f"File not found: {filepath}")
        tree = etree.parse(filepath)
        root = tree.getroot()
        document = cls()
        document.MiscModelVersion = root.get("MiscModelVersion", "131081")
        document.grid = root.get("grid", "1")
        for layout in root.findall("layout"):
            layout_value = layout.get("value")
            group_element = root.find(f"./groups[@identifier='{layout_value}']")
            document.add_group(
                group=Group.from_ptldoc(root=root, element=group_element)
            )
        return document

    def __init__(self):
        self.MiscModelVersion = "131081"
        self.grid = "1"
        self.groups = []

    def add_group(self, group: Group):
        self.groups.append(group)

    def save(self, dest):
        document = etree.Element("document")
        for key, value in self.__dict__.items():
            if not isinstance(value, (list,)):
                document.set(key, value)
        for group in self.groups:
            group.save(document)
        xml = etree.ElementTree(document)
        with open(dest, "wb") as f:
            xml.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    def __str__(self):
        res = {}
        for attribute in self.__dict__:
            if not isinstance(self.__dict__[attribute], (list, Group)):
                res[attribute] = self.__dict__[attribute]
        res["groups"] = [str(group) for group in self.groups]
        return str(res)
