from lxml import etree


class TrackColors:
    @classmethod
    def from_ptldoc(cls, element: etree):
        if element is None:
            return cls()
        colors = cls()
        colors.map = element.get("map", "7")
        colors.background = element.get("background", "0")
        colors.foreground = element.get("foreground", "ff7e7a7d")
        colors.duration = element.get("duration", "667e7a7d")
        colors.text = element.get("text", "0")
        colors.shadow = element.get("shadow", "0")
        return colors

    def __init__(self):
        self.map = "7"
        self.background = "0"
        self.foreground = "ff7e7a7d"
        self.duration = "667e7a7d"
        self.text = "0"
        self.shadow = "0"

    def save(self, track):
        colors = etree.Element("colours")
        for key, value in self.__dict__.items():
            colors.set(key, value)
        track.append(colors)

    def __str__(self):
        return str(self.__dict__)
