"""A class for SdifExporter"""

from .Exporter import Exporter
from ..Document import Document

class SdifExporter(Exporter):
    def __init__(self, exec_path: str, frame: str, matrix: str, colname: str):
        super().__init__(exec_path)
        self.frame = "aaaa"
        self.matrix = "aaaa"
        self.colname = "default"
        self.setFrame(frame)
        self.setMatrix(matrix)
        self.setColname(colname)

    def checkSignature(self, name: str, value: str):
        if type(value) is not str or len(value) != 4:
            return super().error(name, "should be a 4 characters signaturer")
        return 0

    def setFrame(self, value: str):
        """ Set the frame signature

            Args:
                value (str): Defines the 4 characters frame signature
        """
        if self.checkSignature("frame", value):
            return
        self.frame = value

    def setMatrix(self, value: str):
        """ Set the matrix signature

            Args:
                value (str): Defines the 4 characters matrix signature
        """
        if self.checkSignature("matrix", value):
            return
        self.matrix = value

    def setColname(self, value: str):
        """ Set the column's name

            Args:
                value (str): Defines the name of the column
        """
        if type(value) is not str:
            return super().error("colname", "should be a string")
        self.colname = value

    def getCmd(self, Document: Document, output: str):
        res = super().getCmd(Document, output)
        res += [
            "--format=sdif",
            "--frame=" + self.frame,
            "--matrix=" + self.matrix,
            "--colname=" + self.colname
        ]
        return res

    def export(self, Document: Document, output: str):
        """ Export the document

            Args:
                Document (Document): the document to export
                output (str): the destination folder for the export
        """
        cmd = self.getCmd(Document, output)
        return super().export(cmd)
