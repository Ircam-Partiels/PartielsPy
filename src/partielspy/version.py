"""A class for managing version compatibility in PartielsPy"""

import semver


class Version:
    """Compatibility version class for PartielsPy

    This class is used to manage the compatibility versions of PartielsPy with the Partiels\
    executable.
    It provides methods to retrieve the compatibility version and the minimum compatibility\
    versions.
    The versions are defined as a string in semantic versioning format (major.minor.patch).
    The integer representation is calculated by shifting the major, minor, and patch numbers
    to create a single integer value.
    """

    __compatibility_version = "2.1.0"
    __min_compatibility_version = "2.1.0"

    @staticmethod
    def get_compatibility_version() -> str:
        """Return the compatibility version"""
        return Version.__compatibility_version

    @staticmethod
    def get_compatibility_version_int() -> int:
        """Return the integer representation of the compatibility version"""
        version = semver.VersionInfo.parse(Version.__compatibility_version)
        return (version.major << 16) | (version.minor << 8) | (version.patch)

    @staticmethod
    def get_min_compatibility_version() -> str:
        """Return the minimum compatibility version"""
        return Version.__min_compatibility_version

    @staticmethod
    def get_min_compatibility_version_int() -> int:
        """Return the integer representation of the minimum compatibility version"""
        version = semver.VersionInfo.parse(Version.__min_compatibility_version)
        return (version.major << 16) | (version.minor << 8) | (version.patch)


if __name__ == "__main__":
    print(Version.get_compatibility_version())
