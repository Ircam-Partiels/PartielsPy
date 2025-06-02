import json
import subprocess
import uuid

from lxml import etree

from PartielsPy.plugins.description import PluginDescription
from PartielsPy.plugins.key import PluginKey
from PartielsPy.utils import valueToPtldocFormat
from PartielsPy.zoom.zoom import Zoom

from .colors import TrackColors
from .file import TrackFile


class Track:
    @classmethod
    def from_ptldoc(cls, element: etree):
        track = cls()
        track.MiscModelVersion = element.get("MiscModelVersion", "131081")
        track.identifier = element.get("identifier", uuid.uuid4().hex)
        track.name = element.get("name", "New Track")
        track.input = element.get("input", "")
        track.sampleRate = float(element.get("sampleRate", "48000.0"))
        track.height = int(element.get("height", "120"))
        track.font = element.get("font", "Nunito Sans; 14.0 Regular")
        track.lineWidth = float(element.get("lineWidth", "1.0"))
        track.showInGroup = element.get("showInGroup", "1") == "1"
        track.sendViaOsc = element.get("sendViaOsc", "0") == "1"
        track.zoomValueMode = element.get("zoomValueMode", "0") == "1"
        track.zoomLogScale = element.get("zoomLogScale", "0") == "1"
        track.zoomLink = element.get("zoomLink", "1") == "1"
        track.key = PluginKey.from_ptldoc(element.find("key"))
        track.file = TrackFile.from_ptldoc(element.find("file"))
        track.colors = TrackColors.from_ptldoc(element.find("colors"))
        track.valueZoom = Zoom.from_ptldoc(element.find("valueZoom"))
        track.binZoom = Zoom.from_ptldoc(element.find("binZoom"))
        track.description = PluginDescription.from_ptldoc(element.find("description"))
        return track

    @classmethod
    def from_dict(self, data):
        self.MiscModelVersion = 131081
        self.identifier = uuid.uuid4().hex
        self.name = data.get("name", "New Track")
        self.input = ""
        self.sampleRate = 48000.0
        self.height = 120
        self.font = "Nunito Sans; 14.0 Regular"
        self.lineWidth = 1.0
        self.showInGroup = True
        self.sendViaOsc = False
        self.zoomValueMode = False
        self.zoomLogScale = False
        self.zoomLink = True
        self.key = PluginKey.from_dict(data.get("key", {}))
        self.file = TrackFile.from_dict(data.get("file", {}))
        self.colors = TrackColors.from_dict(data.get("colors", {}))
        self.valueZoom = Zoom.from_dict(data.get("valueZoom", {}))
        self.binZoom = Zoom.from_dict(data.get("binZoom", {}))
        self.description = PluginDescription.from_dict(data.get("description", {}))
        # self.description = self.loadPluginDescription(self.key)

    def loadPluginDescription(self, key: PluginKey) -> PluginDescription:
        cmd = [
            "/home/toto/Bureau/IRCAM/Partiels/build/Partiels/Partiels",
            "--plugin-details",
            "--format=json",
            "-i",
            key.identifier,
            "-f",
            key.feature,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return PluginDescription(json.loads(res.stdout))

    def save(self, document, group):
        layout = etree.Element("layout")
        layout.set("value", self.identifier)
        track = etree.Element("tracks")
        for key, value in self.__dict__.items():
            if not isinstance(
                value, (Zoom, TrackFile, TrackColors, PluginKey, PluginDescription)
            ):
                track.set(key, valueToPtldocFormat(value))
        self.key.save(track)
        self.colors.save(track)
        self.valueZoom.save(track, "valueZoom")
        self.binZoom.save(track, "binZoom")
        self.description.saveCurrentState(track)
        self.description.save(track)
        group.append(layout)
        document.append(track)
