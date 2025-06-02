from lxml import etree

from PartielsPy.utils import valueToPtldocFormat


class PluginIO:
    @classmethod
    def from_ptldoc(cls, element: etree):
        if element is None:
            return cls()
        io = cls()
        io.identifier = element.get("identifier", "")
        io.name = element.get("name", "")
        io.description = element.get("description", "")
        io.unit = element.get("unit", "")
        io.hasFixedBinCount = element.get("hasFixedBinCount", "0") == "1"
        io.binCount = int(element.get("binCount", "0"))
        io.hasKnownExtents = element.get("hasKnownExtents", "0") == "1"
        io.minValue = float(element.get("minValue", "0.0"))
        io.maxValue = float(element.get("maxValue", "1.0"))
        io.isQuantized = element.get("isQuantized", "0") == "1"
        io.quantizeStep = float(element.get("quantizeStep", "0.01"))
        io.sampleType = element.get("sampleType", "")
        io.sampleRate = float(element.get("sampleRate", "44100"))
        io.hasDuration = element.get("hasDuration", "0") == "1"
        io.binNames = [bin.get("value") for bin in element.findall("binNames")]
        return io

    @classmethod
    def from_dict(cls, data):
        io = cls()
        io.identifier = data.get("identifier")
        io.name = data.get("name")
        io.description = data.get("description")
        io.unit = data.get("unit")
        io.hasFixedBinCount = data.get("hasFixedBinCount")
        io.binCount = data.get("binCount")
        io.hasKnownExtents = data.get("hasKnownEvents")
        io.minValue = data.get("minValue")
        io.maxValue = data.get("maxValue")
        io.isQuantized = data.get("isQuantized")
        io.quantizeStep = data.get("quantizeStep")
        io.sampleType = data.get("sampleType")
        io.sampleRate = data.get("sampleRate")
        io.hasDuration = data.get("hasDuration")
        io.binNames = data.get("binNames")
        return io

    def save(self, description, tag):
        io = etree.Element(tag)
        for key, value in self.__dict__.items():
            if key != "binNames":
                io.set(key, valueToPtldocFormat(value))
        for bin in self.binNames:
            binName = etree.Element("binNames")
            binName.set("value", valueToPtldocFormat(bin))
            io.append(binName)
        description.append(io)
