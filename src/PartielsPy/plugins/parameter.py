from lxml import etree

from PartielsPy.utils import valueToPtldocFormat


class PluginParameter:
    @classmethod
    def from_ptldoc(cls, element: etree):
        if element is None:
            return cls()
        value = element.find("value")
        parameter = cls()
        parameter.identifier = value.get("identifier", "")
        parameter.name = value.get("name", "")
        parameter.description = value.get("description", "")
        parameter.unit = value.get("unit", "")
        parameter.minValue = float(value.get("minValue", "0.0"))
        parameter.maxValue = float(value.get("maxValue", "1.0"))
        parameter.defaultValue = float(value.get("defaultValue", "0.5"))
        parameter.isQuantized = value.get("isQuantized", "0") == "1"
        parameter.quantizeStep = float(value.get("quantizeStep", "0.01"))
        parameter.valueNames = [v.get("value") for v in value.findall("valueNames")]
        parameter.currentValue = parameter.defaultValue
        return parameter

    @classmethod
    def from_dict(cls, data):
        parameter = cls()
        parameter.identifier = data.get("identifier")
        parameter.name = data.get("name")
        parameter.description = data.get("description")
        parameter.unit = data.get("unit")
        parameter.minValue = data.get("minValue")
        parameter.maxValue = data.get("maxValue")
        parameter.defaultValue = data.get("defaultValue")
        parameter.isQuantized = data.get("isQuantized")
        parameter.quantizeStep = data.get("quantizeStep")
        parameter.valueNames = data.get("valueNames")
        parameter.currentValue = parameter.defaultValue
        return parameter

    def saveValue(self, element, default):
        param = etree.Element("parameters")
        param.set("key", self.identifier)
        if default:
            value = self.defaultValue
        else:
            value = self.currentValue
        param.set("value", valueToPtldocFormat(value))
        element.append(param)

    def save(self, element):
        parameter = etree.Element("parameters")
        pvalue = etree.Element("value")
        for key, value in self.__dict__.items():
            if key != "currentValue" and key != "valueNames":
                pvalue.set(key, valueToPtldocFormat(value))
        parameter.append(pvalue)
        for value in self.valueNames:
            valueName = etree.Element("valueNames")
            valueName.set("value", valueToPtldocFormat(value))
            pvalue.append(valueName)
        element.append(parameter)

    def __str__(self):
        res = {}
        for key, value in self.__dict__.items():
            if key != "currentValue" and key != "valueNames":
                res[key] = value
        return str(res)
