"""A main class for Partiels Wrapper"""

import logging
import os
import platform
import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path

import semver
from lxml import etree

from .document import Document
from .export_config import ExportConfig
from .plugin_list import PluginList
from .version import Version


class Partiels:
    """A class to manage Partiels executable

    The executable path is determined by searching the system's PATH environment variable.
    If the executable is still not found, it checks common installation directories based \
    on the operating system.
    You can use the PARTIELS_PATH environment variable to set the executable path, in this \
    case only the PARTIELS_PATH will be used.
    If the executable is not found, it raises a RuntimeError.
    If the executable is found, its version is compared to the PartielsPy compatibility \
    version and a warning is trigger if not matching.
    If the VAMP_PATH environment variable is set, it will be used to find the VAMP plugins. \
    If not set, the default VAMP plugins directories will be used.
    """

    def __init__(self):
        name = "Partiels"
        if "PARTIELS_PATH" in os.environ:
            self.__executable_path = shutil.which(
                name, path=os.environ.get("PARTIELS_PATH")
            )
        else:
            self.__executable_path = shutil.which(name)
            if self.__executable_path is None:
                if platform.system() == "Linux":
                    self.__executable_path = shutil.which(
                        name, path=os.path.join(os.environ.get("HOME"), "opt")
                    )
                    if self.__executable_path is None:
                        self.__executable_path = shutil.which(name, "/opt")
                elif platform.system() == "Windows":
                    self.__executable_path = shutil.which(
                        name, path=os.path.join(os.environ.get("ProgramW6432"), name)
                    )
                elif platform.system() == "Darwin":
                    self.__executable_path = shutil.which(
                        name,
                        path=os.path.join(
                            "/Applications", name + ".app", "Contents", "MacOS"
                        ),
                    )
        if self.__executable_path is None:
            raise RuntimeError("Executable " + name + " Not Found")
        self.__executable_version = (
            subprocess.run(
                [self.__executable_path, "--version"],
                capture_output=True,
                text=True,
            )
            .stdout.split(" v")[1]
            .strip()
        )
        if semver.VersionInfo.parse(
            Version.get_min_compatibility_version()
        ) > semver.VersionInfo.parse(self.__executable_version):
            raise RuntimeError(
                "PartielsPy minimum compatibility version ("
                + str(Version.get_min_compatibility_version())
                + ") is greater than Partiels's executable version ("
                + str(self.__executable_version)
                + ").\n"
                "Please, update the version of Partiels to compatibility version."
            )
        version_diff = semver.VersionInfo.parse(
            Version.get_compatibility_version()
        ).compare(self.__executable_version)
        if version_diff < 0:
            warnings.warn(
                "PartielsPy compatibility version ("
                + str(Version.get_compatibility_version())
                + ") is older than Partiels's executable version ("
                + str(self.__executable_version)
                + ").\n"
                "Please check if there is a newer version of PartielsPy fully compatible "
                "with the executable version.",
                category=UserWarning,
                stacklevel=2,
            )
        elif version_diff > 0:
            warnings.warn(
                "PartielsPy compatibility version ("
                + str(Version.get_compatibility_version())
                + ") is newer than Partiels's executable version. ("
                + str(self.__executable_version)
                + ").\n"
                "Please, update the version of Partiels to compatibility version.",
                category=UserWarning,
                stacklevel=2,
            )

    @property
    def executable_path(self) -> str:
        """Return Partiels's executable path"""
        return self.__executable_path

    @property
    def executable_version(self) -> str:
        """Return Partiels's executable version"""
        return self.__executable_version

    def export(
        self,
        document: Document,
        output_path: str | Path,
        export_config: ExportConfig,
    ):
        """Export the document to the specified output path using the given export configuration.

        Args:
            document (:class:`Document <partielspy.document>`): the document to export
            output_path (str): the path to the output folder
            export_config (:class:`ExportConfig <partielspy.export_config>`): \
            the export configuration
        """
        if not isinstance(document, Document):
            raise TypeError("Expected a Document instance")
        if not isinstance(export_config, ExportConfig):
            raise TypeError("Expected an ExportConfig instance")
        with tempfile.NamedTemporaryFile(suffix=".ptldoc", delete=False) as temp_file:
            document_path = Path(temp_file.name)
            document.save(document_path)
        cmd = [
            self.__executable_path,
            "--export",
            f"--document={document_path}",
            f"--output={output_path}",
        ]
        cmd += export_config.to_cli_args()
        logging.getLogger(__name__).debug(cmd)
        ret = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if document_path.exists():
            os.remove(document_path)
        return ret

    def get_plugin_list(self) -> PluginList:
        """Get the list of all available plugins from Partiels installed in the VAMP paths
        (defined by the VAMP_PATH environment variable).

        Returns:
            PluginList: A :class:`PluginList <partielspy.plugin_list>` object containing \
            the list of plugins
        """
        cmd = [self.__executable_path, "--plugin-list", "--format=xml"]
        return PluginList._from_xml(
            etree.fromstring(
                subprocess.run(cmd, capture_output=True, text=False, check=True).stdout
            )
        )
