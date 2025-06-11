import os
from pathlib import Path

import pytest

from partielspy import *

root = Path(__file__).parent


def test_basic_creation():
    doc = Document()
    group = Group("Test Group")
    assert group.name == "Test Group", "Group name should be 'Test Group'"
    assert len(group.tracks) == 0, "Group should initially have no tracks"
    track = Track("Test Track")
    assert track.name == "Test Track", "Track name should be 'Test Track'"
    group.add_track(track)
    assert len(group.tracks) == 1, "Group should have one track after adding"
    doc.add_group(group)
    assert len(doc.groups) == 1, "Document should have one group after adding"
    output = root / "templates" / "test_basic_creation.ptldoc"
    if output.exists():
        os.remove(output)
    Partiels().document_to_xml(doc, output)
    assert output.exists(), "Output file was not created"
    group.remove_track(track)
    assert len(group.tracks) == 0, "Group should have no tracks after removal"
    doc.remove_group(group)
    assert len(doc.groups) == 0, "Document should have no groups after removal"


def test_basic_errors():
    doc = Document()
    group = Group("Group")
    track = Track("Track")

    with pytest.raises(TypeError):
        doc.add_group("dummy"), "Should raise TypeError when adding non-Group instance"
    with pytest.raises(TypeError):
        group.add_track(
            "dummy"
        ), "Should raise TypeError when adding non-Track instance"
    with pytest.raises(ValueError):
        doc.remove_group(
            group
        ), "Should raise ValueError when removing non-existent group"
    with pytest.raises(ValueError):
        group.remove_track(
            track
        ), "Should raise ValueError when removing non-existent track"
