import copy
import uuid

from lxml import etree

from .track import Track
from .version import Version


class Group:
    def __init__(self, name: str = "New Group"):
        self.__xml_node = etree.Element("groups")
        self.__name = name
        self.__tracks = {}

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
        res.__tracks = {
            uuid.uuid4().hex: copy.deepcopy(track, memo) for track in self.tracks
        }
        return res

    def _from_xml(self, node: etree.Element):
        self.name = node.get("name", self.name)
        track_layouts = node.findall("layout")
        for track_layout in track_layouts:
            track_layout_value = track_layout.get("value")
            track_node = node.getparent().find(
                f"./tracks[@identifier='{track_layout_value}']"
            )
            track = Track()
            track._from_xml(track_node)
            self.__tracks[track_layout_value] = track
            node.remove(track_layout)
            node.getparent().remove(track_node)
        self.__xml_node = copy.deepcopy(node)

    def _to_xml(self, identifier: str) -> list[etree.Element]:
        all_nodes = []
        node = copy.deepcopy(self.__xml_node)
        node.set("MiscModelVersion", Version.get_compatibility_version_int())
        node.set("identifier", identifier)
        node.set("name", self.__name)
        all_nodes.append(node)
        for track_identifier, track in self.__tracks.items():
            layout = etree.Element("layout")
            layout.set("value", track_identifier)
            node.append(layout)
            all_nodes.append(track._to_xml(track_identifier))
        return all_nodes
