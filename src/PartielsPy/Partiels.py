"""A main class for Partiels Wrapper"""

import os
import platform
import shutil
import subprocess
import semver


class Partiels:
    def __init__(self):
        """Initialize Partiels executable path and version

        The executable path is determined by searching the system's PATH environment variable.
        If the executable is still not found, it checks common installation directories based \
        on the operating system.
        You can use the PARTIELS_PATH environment variable to set the executable path, in this \
        case only the PARTIELS_PATH will be used.
        If the executable is not found, it raises a RuntimeError.
        If the executable is found, its version is compared to the PartielsPy compatibility \
        version and a warning is trigger if not matching.
        """
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
            print(
                "Warning: PartielsPy version is older than Partiels's executable version.\n"
                "Please, check if there is a newer version of PartielsPy fully compatible \
                with the executable version"
            )
        elif version_diff > 0:
            print(
                "Warning: PartielsPy version is newer than Partiels's executable version.\n"
                "Please, update the version of Partiels to compatibility version:",
                self.__compatibility_version,
            )

    def getExecutablePath(self):
        """Return Partiels's executable path"""

        return self.__executable_path

    def getExecutableVersion(self):
        """Return Partiels's executable version"""

        return self.__executable_version

    def getCompatibilityVersion(self):
        """Return the PartielsPy's compatibility version"""

        return self.__compatibility_version
