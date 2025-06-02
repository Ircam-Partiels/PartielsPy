import uuid

from lxml import etree

from PartielsPy.track.track import Track
from PartielsPy.zoom.zoom import Zoom


class Group:
    @classmethod
    def from_ptldoc(cls, root: etree, element: etree):
        group = cls()
        group.MiscModelVersion = element.get("MiscModelVersion", "131081")
        group.identifier = element.get("identifier", uuid.uuid4().hex)
        group.name = element.get("name", "New Group")
        group.height = element.get("height", "144")
        group.colour = element.get("colour", "0")
        group.expanded = element.get("expanded", "1")
        group.referenceid = element.get("referenceid", "")
        group.zoom = Zoom.from_ptldoc(element=element.find("zoom"))

        for layout in element.findall("layout"):
            identifier = layout.get("value")
            track_element = root.find(f"./tracks[@identifier='{identifier}']")
            group.add_track(Track.from_ptldoc(track_element))
        return group

    def __init__(self, name: str = "New Group"):
        self.MiscModelVersion = "131081"
        self.identifier = uuid.uuid4().hex
        self.name = name
        self.height = "144"
        self.colour = "0"
        self.expanded = "1"
        self.referenceid = ""
        self.zoom = Zoom()
        self.tracks = []

    def add_track(self, track: Track):
        self.tracks.append(track)

    def save(self, document):
        layout = etree.Element("layout")
        layout.set("value", self.identifier)
        group = etree.Element("groups")
        for key, value in self.__dict__.items():
            if not isinstance(value, (Zoom, list)):
                group.set(key, value)
        self.zoom.save(group, "zoom")
        for track in self.tracks:
            track.save(document, group)
        document.append(layout)
        document.append(group)

    def __str__(self):
        res = {}
        for attribute in self.__dict__:
            if not isinstance(
                self.__dict__[attribute],
                (
                    Zoom,
                    list,
                ),
            ):
                res[attribute] = self.__dict__[attribute]
        res["zoom"] = str(self.zoom)
        return str(res)
