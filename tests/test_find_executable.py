from partielspy.partiels import Partiels


def test_find_executable():
    assert Partiels().executable_path is not None, "Partiels Executable not found"
    print(Partiels().executable_path + " v" + Partiels().executable_version)
