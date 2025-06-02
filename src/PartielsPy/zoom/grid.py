from lxml import etree


class ZoomGrid:
    @classmethod
    def from_ptldoc(cls, element: etree):
        grid = cls()
        grid.MiscModelVersion = element.get("MiscModelVersion", "131081")
        grid.tickReference = element.get("tickReference", "0.0")
        grid.mainTickInterval = element.get("mainTickInterval", "3")
        grid.tickPowerBase = element.get("tickPowerBase", "2.0")
        grid.tickDivisionFactor = element.get("tickDivisionFactor", "5.0")
        return grid

    def __init__(self):
        self.MiscModelVersion = "131081"
        self.tickReference = "0.0"
        self.mainTickInterval = "3"
        self.tickPowerBase = "2.0"
        self.tickDivisionFactor = "5.0"

    def save(self, element):
        grid = etree.Element("grid")
        for key, value in self.__dict__.items():
            grid.set(key, value)
        element.append(grid)

    def __str__(self):
        return str(self.__dict__)
