"""A class for managing version compatibility in PartielsPy"""

import semver


class Version:
    """Compatibility version class for PartielsPy

    This class is used to manage the compatibility version of PartielsPy \
    with the Partiels executable.
    It provides methods to retrieve the compatibility version as a string and as an integer.
    The compatibility version is defined as a string in semantic versioning \
    format (major.minor.patch).
    The integer representation is calculated by shifting the major, minor, and patch numbers
    to create a single integer value.
    """

    __compatibility_version = "2.1.0"

    @staticmethod
    def get_compatibility_version() -> str:
        """Return the compatibility version"""
        return Version.__compatibility_version

    @staticmethod
    def get_compatibility_version_int() -> str:
        """Return the integer representation of the compatibility version"""
        version = semver.VersionInfo.parse(Version.__compatibility_version)
        return (version.major << 16) | (version.minor << 8) | (version.patch)


if __name__ == "__main__":
    print(Version.get_compatibility_version())
