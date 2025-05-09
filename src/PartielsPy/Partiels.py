"""A main class for Partiels Wrapper"""

from pathlib import Path
#from lxml import etree
import os
import shutil
import json
import subprocess
from .Version import Version
from .Document import Document
from .Exporters.ImageExporter import ImageExporter
from .Exporters.TextExporter import CsvExporter, JsonExporter, CueExporter, ReaperExporter, LabExporter
from .Exporters.SdifExporter import SdifExporter

PARTIELS_HANDLED_VERSION_MIN = "2.0.9"
PARTIELS_HANDLED_VERSION_MAX = "2.0.10"

class Partiels():

    def __init__(self):
        self.setExecPath(self.findExecPath())
        self.isHandledVersion = self.checkVersion()

    def getExecPath(self):
        """Return the executable path of Partiels"""
        return self.exec_path

    def setExecPath(self, path: str):
        """Set the path for Partiels's executable
        
            Args:
                path (str): relative or absolute path
        """
        self.exec_path = path

    def setVampPath(self, path: str):
        os.environ["VAMP_PATH"] = path

    def findExecPath(self):
        "Find Partiels's executable path"
        exec_name = "Partiels"
        exec_path = shutil.which(exec_name)
        if exec_path:
            return exec_path
        else:
            print(f"Executable '{exec_name}' non trouvé dans PATH.")
        return None

    def checkVersion(self):
        """Check if the wrapper match Partiels's version"""

        cmd = [self.exec_path, "--version"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        version = Version.from_string(res.stdout.split(" v")[1][:-1])
        min = Version.from_string(PARTIELS_HANDLED_VERSION_MIN)
        max = Version.from_string(PARTIELS_HANDLED_VERSION_MAX)

        if version is None:
            print("Error parsing Partiels version")
            return False
        if version.isMoreRecent(max):
            print("The Version of Partiel is too recent for the wrapper")
            return False
        if min.isMoreRecent(version):
            print("The Version of Partiel is too old for the wrapper")
            return False
        return True

    def createDocument(self, input:str, template:str):
        """Create a Document

            Args:
                input (str): relative or absolute path of the audiofile
                template (str): relative or absolute path of the template (ptldoc)
        """
        return Document(input, template)

    def createDefaultDocument(self, input:str, template:str):
        """Create a Document with a default template

            Args:
                input (str): relative or absolute path of the audiofile
                template (str): name of the default template. Options ar factory, supervp or partiels
        """
        return Document(input, template, True)

    def createJpegExporter(self, width:int = 1000, height:int = 800, groups:bool = False):
        """Create a JpegExporter

            Args:
                width (int): the width of the target jpeg image
                height (int): the height of the target jpeg image
                groups (bool): if True exports the images of group and not the image of the tracks 
        """
        return ImageExporter(self.exec_path, "jpeg", width, height, groups)

    def createPngExporter(self, width:int = 1000, height:int = 800, groups:bool = False):
        """Create a PngExporter

            Args:
                width (int): the width of the target png image
                height (int): the height of the target png image
                groups (bool): if True exports the images of group and not the image of the tracks 
        """
        return ImageExporter(self.exec_path, "png", width, height, groups)

    def createCsvExporter(self, nogrids:bool = False, header:bool = False, separator:str = ","):
        """Create a CsvExporter
        
            Args:
                nogrids (bool): if True ignores the export of the grid tracks
                header (bool): if True includes header row before the data rows
                separator (char): Defines the separator character between columns (default is ',')
        """
        return CsvExporter(self.exec_path, nogrids, header, separator)

    def createReaperExporter(self, reaperType:str = "region"):
        """Create a ReaperExporter
        
            Args:
                reaperType (str): Defines the type of the reaper format: 'marker' or 'region', default is 'region'.
        """
        return ReaperExporter(self.exec_path, reaperType)

    def createLabExporter(self):
        """Create a LabExporter"""
        return LabExporter(self.exec_path)
        
    def createJsonExporter(self, nogrids:bool = False, description:bool = False):
        """Create a JsonExporter
        
            Args:
                nogrids (bool): if True ignores the export of the grid tracks
                description (bool): if True includes the plugin description 
        """
        return JsonExporter(self.exec_path, nogrids, description)

    def createCueExporter(self, nogrids:bool = False):
        """Create a CueExporter
        
            Args:
                nogrids (bool): if True ignores the export of the grid tracks
        """
        return CueExporter(self.exec_path, nogrids)

    def createSdifExporter(self, frame:str = None, matrix:str = None, colname:str = None):
        """Create a SdifExporter
        
            Args:
                frame (str): <framesignature> Defines the 4 characters frame signaturer
                matrix (str): <matrixsignature> Defines the 4 characters matrix signaturer
                colname (str): Defines the name of the column
        """
        return SdifExporter(self.exec_path, frame, matrix, colname)



