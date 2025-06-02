from lxml import etree

from PartielsPy.utils import valueToPtldocFormat


class PluginState:
    @classmethod
    def from_ptldoc(cls, element: etree):
        if element is None:
            return cls()
        state = cls()
        state.blockSize = int(element.get("blockSize", "64"))
        state.stepSize = int(element.get("stepSize", "1"))
        state.windowType = element.get("windowType", "Hamming")
        return state

    @classmethod
    def from_dict(cls, data):
        state = cls()
        state.blockSize = data.get("blockSize")
        state.stepSize = data.get("stepSize")
        state.windowType = data.get("windowType")
        return state

    def addAttributeToSave(self, element):
        for key, value in self.__dict__.items():
            element.set(key, valueToPtldocFormat(value))

    def save(self, element, parameters, tag):
        state = etree.Element(tag)
        self.addAttributeToSave(state)
        for parameter in parameters:
            parameter.saveValue(state, (tag == "defaultValue"))
        element.append(state)
