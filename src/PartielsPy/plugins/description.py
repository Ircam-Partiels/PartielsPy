from lxml import etree

from PartielsPy.utils import valueToPtldocFormat

from .io import PluginIO
from .parameter import PluginParameter
from .state import PluginState


class PluginDescription:
    @classmethod
    def from_ptldoc(cls, element: etree):
        if element is None:
            return cls()
        description = cls()
        description.name = element.get("name", "")
        description.inputDomain = element.get("inputDomain", "")
        description.maker = element.get("maker", "")
        description.version = element.get("version", "")
        description.category = element.get("category", "")
        description.details = element.get("details")
        description.defaultState = PluginState.from_ptldoc(element.find("defaultState"))
        description.currentState = description.defaultState
        description.parameters = []
        for parameter in element.findall("parameters"):
            p = PluginParameter.from_ptldoc(parameter)
            description.parameters.append(p)

        description.input = PluginIO.from_ptldoc(element.find("input"))
        description.output = PluginIO.from_ptldoc(element.find("output"))
        return description

    @classmethod
    def from_dict(cls, data: dict):
        description = cls()
        description.name = data.get("name")
        description.inputDomain = data.get("inputDomain")
        description.maker = data.get("maker")
        description.version = data.get("version")
        description.category = data.get("category", "")
        description.details = data.get("details")
        description.defaultState = PluginState.from_dict(data.get("defaultState"))
        description.currentState = description.defaultState
        description.parameters = []
        for parameter in data.get("parameters"):
            description.parameters.append(PluginParameter.from_dict(parameter))
        description.input = PluginIO.from_dict(data.get("input"))
        description.output = PluginIO.from_dict(data.get("output"))
        return description

    def saveCurrentState(self, element):
        self.currentState.save(element, self.parameters, "state")

    def saveDefaultState(self, element):
        self.defaultState.save(element, self.parameters, "defaultState")

    def save(self, track):
        description = etree.Element("description")
        for key, value in self.__dict__.items():
            if not isinstance(value, (PluginState, PluginIO, list)):
                description.set(key, valueToPtldocFormat(value))
        self.saveDefaultState(description)
        for parameter in self.parameters:
            parameter.save(description)
        self.input.save(description, "input")
        self.output.save(description, "output")
        track.append(description)
