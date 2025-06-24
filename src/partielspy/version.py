import semver


class Version:
    __compatibility_version = "2.0.12-dev2"

    @staticmethod
    def get_compatibility_version():
        return Version.__compatibility_version

    @staticmethod
    def get_compatibility_version_int():
        version = semver.VersionInfo.parse(Version.__compatibility_version)
        return str((version.major << 16) | (version.minor << 8) | (version.patch))


if __name__ == "__main__":
    print(Version.get_compatibility_version())
