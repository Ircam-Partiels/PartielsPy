"""A class for ImageExporter, used for jpeg and png formats"""

from .Exporter import Exporter
from ..Document import Document

class ImageExporter(Exporter):
    
    def __init__(self, exec_path, format, width, height, groups):
        super().__init__(exec_path)
        self.width = 1000
        self.height = 800
        self.groups = False
        if self.setFormat(format):
            self.format = "jpeg"
        self.setWidth(width)
        self.setHeight(height)
        self.setGroups(groups)

    '''
    def setFormat(self, format: str):
        valid_formats = ["jpeg", "png"]
        format = format.lower()
        if format not in valid_formats:
            return super().error("format", format + " is not a valid format. Valid formats are" + valid_formats)
        self.format = format
        return 0
    '''
    
    def setDimension(self, name: str, value: int):
        if value < 1:
            return self.error(f"set{name.capitalize()}", "value must be greater than 0")
        setattr(self, name.lower(), value)
        return 0

    def setWidth(self, width: int):
        return self.setDimension("width", width)

    def setHeight(self, height: int):
        return self.setDimension("height", height)

    def setGroups(self, value: bool):
        """ Set the groups option

            Args:
                value (bool): if True exports the images of group and not the image of the tracks
        """
        if super().checkBoolAttr("groups", value):
            return
        self.groups = value

    def getCmd(self, Document: Document, output: str):
        res = super().getCmd(Document, output)
        res += [
            "--format=" + self.format,
            "--width=" + str(self. width),
            "--height=" + str(self.height)
            ]
        if self.groups:
            res.append("--groups")
        return res

    def export(self, Document: Document, output: str):
        """ Export the document

            Args:
                Document (Document): the document to export
                output (str): the destination folder for the export
        """
        cmd = self.getCmd(Document, output)
        return super().export(cmd)