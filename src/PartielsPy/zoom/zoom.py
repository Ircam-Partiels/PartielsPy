from lxml import etree

from .grid import ZoomGrid


class Zoom:
    @classmethod
    def from_ptldoc(cls, element: etree):
        zoom = cls()
        zoom.MiscModelVersion = element.get("MiscModelVersion", "131081")
        zoom.globalRange_start = element.get("globalRange_start", "0.0")
        zoom.globalRange_end = element.get("globalRange_end", "0.0")
        zoom.minimumLength = element.get("minimumLength", "0.0")
        zoom.visibleRange_start = element.get("visibleRange_start", "0.0")
        zoom.visibleRange_end = element.get("visibleRange_end", "0.0")
        zoom.grid = ZoomGrid.from_ptldoc(element.find("grid"))
        return zoom

    def __init__(self):
        self.MiscModelVersion = "131081"
        self.globalRange_start = "0.0"
        self.globalRange_end = "0.0"
        self.minimumLength = "0.0"
        self.visibleRange_start = "0.0"
        self.visibleRange_end = "0.0"
        self.grid = ZoomGrid()

    def save(self, element, tag):
        zoom = etree.Element(tag)
        for key, value in self.__dict__.items():
            if key != "grid":
                zoom.set(key, value)
        self.grid.save(zoom)
        element.append(zoom)

    def __str__(self):
        res = {}
        for attribute in self.__dict__:
            if not isinstance(self.__dict__[attribute], ZoomGrid):
                res[attribute] = self.__dict__[attribute]
        res["grid"] = str(self.grid)
        return str(res)
