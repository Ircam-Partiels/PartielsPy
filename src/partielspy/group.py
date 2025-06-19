import copy
import uuid

from lxml import etree

from .track import Track
from .version import Version
from .xml_element import XmlElement


class Group(XmlElement):
    __ignored_attributes = ["identifier", "name"]
    __ignored_children = ["layout"]

    def __init__(self, name: str = "New Group"):
        self.__name = name
        self.__tracks = {}
        super().__init__(
            ignored_attributes=Group.__ignored_attributes,
            ignored_children=Group.__ignored_children,
        )

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def tracks(self) -> list[Track]:
        return list(self.__tracks.values())

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise TypeError("Expected a Track instance")
        if track in self.tracks:
            raise ValueError("Track already exists in group")
        self.__tracks[uuid.uuid4().hex] = track

    def remove_track(self, track: Track):
        for identifier, value in self.__tracks.items():
            if track == value:
                del self.__tracks[identifier]
                return
        raise ValueError("Track not found in group")

    def __deepcopy__(self, memo):
        res = type(self)(self.__name)
        super(type(self), res).__deepcopy__(memo)
        res.__tracks = {
            uuid.uuid4().hex: copy.deepcopy(track, memo) for track in self.tracks
        }
        return res

    @classmethod
    def _from_xml(cls, node: etree):
        group = cls()
        group.from_xml(node)
        group.name = node.get("name", "New Group")
        for track_layout in node.findall("layout"):
            track_layout_value = track_layout.get("value")
            track_node = node.getparent().find(
                f"./tracks[@identifier='{track_layout_value}']"
            )
            group.__tracks[track_layout_value] = Track._from_xml(track_node)
        return group

    def _to_xml(self, node: etree):
        super().to_xml(node)
        node.set("name", self.__name)
        for identifier, track in self.__tracks.items():
            layout = etree.Element("layout")
            node.append(layout)
            layout.set("value", identifier)
            track_node = etree.Element("tracks")
            node.getparent().append(track_node)
            track_node.set("identifier", identifier)
            track_node.set("MiscModelVersion", Version.get_compatibility_version_int())
            track._to_xml(track_node)

    def _to_json(self) -> dict:
        res = {"name": self.name, "tracks": []}
        for track in self.tracks:
            res["tracks"].append(track._to_json())
        return res
