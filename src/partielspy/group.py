import uuid

from lxml import etree

from partielspy.track import Track


class Group:
    def __init__(self, name: str = "New Group"):
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
        self.__tracks[uuid.uuid4().hex] = track

    def remove_track(self, track: Track):
        for identifier, value in self.__tracks.items():
            if track == value:
                del self.__tracks[identifier]
                return
        raise ValueError("Track not found in group")

    def _to_xml(self, node: etree):
        node.set("name", self.__name)
        node.getparent().set("value", self.__name)
        for track_identifier, track in self.__tracks.items():
            layout_node = etree.Element("layout")
            layout_node.set("value", track_identifier)
            node.append(layout_node)
            track_node = etree.Element("tracks")
            track_node.set("identifier", track_identifier)
            track._to_xml(track_node)
            node.getparent()._to_xml(track_node)

    def _to_xml(self, node: etree):
        node.set("name", self.__name)

    def __str__(self):
        res = self.name + ": "
        for track in self.tracks:
            res += track.__str__()
            res += ", " if track != self.tracks[-1] else ""
        return res
