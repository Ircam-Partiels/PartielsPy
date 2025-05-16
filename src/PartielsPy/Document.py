"""A class for Document"""

import pkg_resources


class Document:
    """A class for Document

    The Document class is used to create a document for the Partiels software.
    It contains the audiofile path and the template path.
    The template path can be set to a default template or a custom template.
    The default templates are:
    - factory
    - harmonic_partials_tracking
    - waveform_fft
    """

    def __init__(self, audiofile: str, template: str, isDefault: bool = False):
        self.__audiofile = audiofile
        self.setTemplate(template, isDefault)

    @property
    def audiofile(self):
        """Get the audiofile path"""
        return self.__audiofile

    @audiofile.setter
    def audiofile(self, path: str):
        """Set the audiofile path

        Args:
            path (str): absolute ot relative path for the audiofile
        """
        self.__audiofile = path

    @property
    def template(self):
        """Get the Partiels's template path"""
        return self.__template

    def setTemplate(self, path: str, isDefault: bool = False):
        """Set the Partiels's template path

        Args:
            path (str): absolute ot relative path for the audiofile
            isDefault (bool): if True the path is used to select a default
                template: factory, harmonic_partials_tracking, waveform_fft
        """
        if isDefault:
            self.__template = pkg_resources.resource_filename(
                __name__, "templates/" + path + ".ptldoc"
            )
        else:
            self.__template = path

    def getArgs(self):
        """Get the arguments for the command line

        Returns:
            list: list of arguments for the command line
        """
        return [
            "--input=" + self.__audiofile,
            "--template=" + self.__template,
        ]
