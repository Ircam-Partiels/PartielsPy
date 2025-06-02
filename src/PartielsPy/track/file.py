from lxml import etree


class TrackFile:
    @classmethod
    def from_ptldoc(cls, element: etree):
        if element is None:
            return cls()
        track_file = cls()
        track_file.path = element.get("path", "")
        track_file.commit = element.get("commit", "")
        return track_file

    def __init__(self, path: str = "", commit: str = ""):
        self.path = path
        self.commit = commit

    def __str__(self):
        return f"TrackFile(path={self.path}, commit={self.commit})"
