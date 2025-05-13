from ..src.PartielsPy.Partiels import Partiels


def test_find_executable():
    assert Partiels().getExecutablePath() is not None, "Partiels Executable not found"
    print(Partiels().getExecutablePath() + " v" + Partiels().getExecutableVersion())
