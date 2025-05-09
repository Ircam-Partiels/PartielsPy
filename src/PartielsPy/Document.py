"""A class for Document"""

import pkg_resources

class Document():
    def __init__(self, input: str, template: str, isDefault: bool = False):
        self.setInput(input)
        self.setTemplate(template, isDefault)

    def setInput(self, path: str):
        """ Set the audiofile input path

            Args:
                path (str): absolute ot relative path for the audiofile
        """
        self.input = path

    def setTemplate(self, path: str, isDefault: bool = False):
        """ Set the Partiels's template path

            Args:
                path (str): absolute ot relative path for the audiofile
                isDefault (bool): if True the path is used to select a default template: factory, partiels, supervp 
        """
        if isDefault:
            self.template = pkg_resources.resource_filename(__name__, 'templates/'+ path +'.ptldoc')
        else:
            self.template = path

    def getArgs(self):
        return [
            "--input=" + self.input,
            "--template=" + self.template,
        ]