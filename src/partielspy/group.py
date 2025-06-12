import uuid

from lxml import etree

from partielspy.track import Track


class Group:
    def __init__(self, name: str = "New Group"):
        self.__name = name
        self.__tracks = {}
        self.__xml_attributes = {}
        self.__xml_children = []

    @classmethod
    def _from_xml(cls, node: etree):
        group = cls(node.get("name", "New Group"))
        group.__xml_attributes = node.attrib
        for child in node:
            if child.tag != "layout":
                group.__xml_children.append(child)
        return group

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def tracks(self) -> list[Track]:
        return list(self.__tracks.values())

    @property
    def _tracks_items(self) -> dict[str, Track]:
        return self.__tracks

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise TypeError("Expected a Track instance")
        self.__tracks[uuid.uuid4().hex] = track

    def remove_track(self, track: Track):
        for identifier, value in self.__tracks.items():
            if track == value:
                del self.__tracks[identifier]
                return
        raise ValueError("Track not found in group")

    def _to_xml(self, node: etree):
        for key, value in self.__xml_attributes.items():
            node.set(key, value)
        for child in self.__xml_children:
            node.append(child)
        node.set("name", self.__name)

    def __str__(self):
        res = self.name + ": "
        for track in self.tracks:
            res += track.__str__()
            res += ", " if track != self.tracks[-1] else ""
        return res
