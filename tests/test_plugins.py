from pathlib import Path

from partielspy import *

root = Path(__file__).parent


def test_plugin_list():
    least_expected = [
        ["partiels-vamp-plugins:partielswaveform", "peaks"],
        ["partiels-vamp-plugins:partielsspectrogram", "energies"],
    ]

    key_list = Partiels().plugin_list()

    def check_plugin(expected):
        for plugin in key_list:
            if plugin.identifier == expected[0] and plugin.feature == expected[1]:
                return True

    for expected in least_expected:
        assert check_plugin(expected), f"Plugin {expected} not found in PluginList"
