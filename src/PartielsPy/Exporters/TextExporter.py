"""classes for TextExporter"""


from .Exporter import Exporter
from ..Document import Document

class TextExporter(Exporter):
    def __init__(self, exec_path: str, nogrids: bool):
        super().__init__(exec_path)
        self.nogrids = False
        self.setNogrids(nogrids)

    def setNogrids(self, value: bool):
        """ Set the nogrids option

            Args:
                value (bool): if True ignores the export of the grid tracks
        """
        if super().checkBoolAttr("nogrids", value):
            return
        self.nogrids = value

    def getCmd(self, Document: Document, output: str):
        res = super().getCmd(Document, output)
        if self.nogrids:
            res.append("--nogrids")
        return res

    def export(self, cmd: list[str]):
        return super().export(cmd)


class CsvExporter(TextExporter):
    def __init__(self, exec_path: str, nogrids: bool, header: bool, separator: str):
        super().__init__(exec_path, nogrids)
        self.header = False
        self.separator = ","
        self.setHeader(header)
        self.setSeparator(separator)

    def setHeader(self, value: bool):
        """ Set the header option

            Args:
                value (bool): if True includes header row before the data rows
        """
        if super().checkBoolAttr("header", value):
            return
        self.header = value

    def setSeparator(self, value: str):
        """ Set the separator character

            Args:
                value (str): Defines the separator character between columns
        """
        if type(value) is not str and len(value) != 1:
            return self.error("character", "value is not valid")
        self.separator = value

    def getCmd(self, Document: Document, output: str):
        res = super().getCmd(Document, output)
        res += [
            "--format=csv",
            "--separator=" + self.separator
            ]
        if self.header:
            res.append("--header")
        return res

    def export(self, Document: Document, output: str):
        cmd = self.getCmd(Document, output)
        return super().export(cmd)


class ReaperExporter(Exporter): # csv egalement
    def __init__(self, exec_path: str, reaperType: str):
        super().__init__(exec_path)
        if self.setReaperType(reaperType):
            self.reaper_type = "region"

    def setReaperType(self, value: str):
        """ Set the reapertype

            Args:
                value (str): Defines the type of the reaper format ('marker' or 'region', default is 'region')
        """
        if value != "region" and value != "marker":
            return super().error("reapertype", "should be region or marker")
        self.reaper_type = value

    def getCmd(self, Document: Document, output: str):
        res = super().getCmd(Document, output)
        res += [
            "--format=reaper",
            "--reapertype=" + self.reaper_type,
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


class LabExporter(TextExporter):
    def __init__(self, exec_path: str, nogrids: bool):
        super().__init__(exec_path, nogrids)

    def getCmd(self, Document: Document, output: str):
        res = super().getCmd(Document, output)
        res.append("--format=lab")
        return res
    
    def export(self, Document: Document, output: str):
        """ Export the document

            Args:
                Document (Document): the document to export
                output (str): the destination folder for the export
        """
        cmd = self.getCmd(Document, output)
        return super().export(cmd)


class JsonExporter(TextExporter):
    def __init__(self, exec_path: str, nogrids: bool, description: bool):
        super().__init__(exec_path, nogrids)
        self.description = False
        self.setDescription(description)

    def setDescription(self, value: bool):
        """ Set the description option

            Args:
                value (bool): if True includes the plugin description
        """
        if super().checkBoolAttr("description", value):
            return
        self.description = value

    def getCmd(self, Document: Document, output: str):
        res = super().getCmd(Document, output)
        res.append("--format=json")
        if self.description:
            res.append("--description")
        return res

    def export(self, Document: Document, output: str):
        """ Export the document

            Args:
                Document (Document): the document to export
                output (str): the destination folder for the export
        """
        cmd = self.getCmd(Document, output)
        return super().export(cmd)


class CueExporter(TextExporter):
    def __init__(self, exec_path: str, nogrids: bool):
        super().__init__(exec_path, nogrids)

    def getCmd(self, Document: Document, output: str):
        res = super().getCmd(Document, output)
        res.append("--format=cue")
        return res
    
    def export(self, Document: Document, output: str):
        """ Export the document

            Args:
                Document (Document): the document to export
                output (str): the destination folder for the export
        """
        cmd = self.getCmd(Document, output)
        return super().export(cmd)
