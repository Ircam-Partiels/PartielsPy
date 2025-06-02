from lxml import etree


class PluginKey:
    @classmethod
    def from_ptldoc(cls, element: etree):
        key = cls()
        key.identifier = element.get("identifier")
        key.feature = element.get("feature")
        return key

    @classmethod
    def from_dict(cls, data):
        key = cls()
        key.identifier = data.get("identifier")
        key.feature = data.get("feature")
        return key

    def __str__(self):
        return f"PluginKey(identifier={self.identifier}, feature={self.feature})"

    def save(self, track):
        pkey = etree.Element("key")
        for key, value in self.__dict__.items():
            pkey.set(key, value)
        track.append(pkey)
