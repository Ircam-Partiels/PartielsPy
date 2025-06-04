"""A main class for Partiels Wrapper"""

import logging
import os
import platform
import shutil
import subprocess
import warnings
from pathlib import Path

import semver

from .export_configs.base import ExportConfigBase


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
    For each call to the Partiels's CLI The VAMP_PATH environment variable is set to include \
    the Partiels plugins. If the VAMP_PATH environment variable is already set, it is \
    prepended to the Partiels plugins path. If not set, the default VAMP plugins directories \
    are used.
    """

    def __init__(self):
        name = "Partiels"
        self.__compatibility_version = "2.0.10"
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
        version_diff = semver.VersionInfo.parse(self.__compatibility_version).compare(
            self.__executable_version
        )
        if version_diff < 0:
            warnings.warn(
                "PartielsPy compatibility version ("
                + str(self.__compatibility_version)
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
                + str(self.__compatibility_version)
                + ") is newer than Partiels's executable version. ("
                + str(self.__executable_version)
                + ").\n"
                "Please, update the version of Partiels to compatibility version.",
                category=UserWarning,
                stacklevel=2,
            )

    def __substitute_vamp_path(self):
        self.__vamp_path_backup = os.environ.get("VAMP_PATH", "")
        if platform.system() == "Linux":
            partiels_plugins_path = "/opt/Partiels/PlugIns"
            vamp_plugins_paths = [
                os.path.join(os.environ.get("HOME"), "vamp"),
                os.path.join(os.environ.get("HOME"), ".vamp"),
                "/usr/local/lib/vamp",
                "/usr/lib/vamp",
            ]
            separator = ":"
        elif platform.system() == "Windows":
            partiels_plugins_path = os.path.join(
                os.environ.get("ProgramFiles"), "Partiels", "PlugIns"
            )
            vamp_plugins_paths = [
                os.path.join(os.environ.get("ProgramFiles"), "Vamp Plugins")
            ]
            separator = ";"
        elif platform.system() == "Darwin":
            partiels_plugins_path = "/Applications/Partiels.app/Contents/PlugIns"
            vamp_plugins_paths = [
                os.path.join(os.environ.get("HOME"), "Library/Audio/Plug-Ins/Vamp"),
                "/Library/Audio/Plug-Ins/Vamp",
            ]
            separator = ":"
        else:
            return
        if self.__vamp_path_backup != "":
            path = separator.join([partiels_plugins_path, self.__vamp_path_backup])
        else:
            vamp_plugins_paths.insert(0, partiels_plugins_path)
            path = separator.join(vamp_plugins_paths)
        os.environ["VAMP_PATH"] = path

    @property
    def executable_path(self) -> str:
        """Return Partiels's executable path"""
        return self.__executable_path

    @property
    def executable_version(self) -> str:
        """Return Partiels's executable version"""
        return self.__executable_version

    @property
    def compatibility_version(self) -> str:
        """Return the PartielsPy's compatibility version"""
        return self.__compatibility_version

    def export(
        self,
        audiofile_path: str | Path,
        template_path: str | Path,
        output_path: str | Path,
        export_config: ExportConfigBase,
    ):
        """Export the audiofile with the template and export configuration

        Args:
            audiofile_path (str): the path to the audio file
            template_path (str): the path to the template
            output_path (str): the path to the output folder
            export_config (ExportConfigBase): the export configuration
        """
        cmd = [
            self.__executable_path,
            "--export",
            f"--input={audiofile_path}",
            f"--template={template_path}",
            f"--output={output_path}",
        ]
        cmd += export_config.to_cli_args()
        logging.getLogger(__name__).debug(cmd)
        self.__substitute_vamp_path()
        try:
            ret = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            raise
        finally:
            os.environ["VAMP_PATH"] = self.__vamp_path_backup
        return ret
