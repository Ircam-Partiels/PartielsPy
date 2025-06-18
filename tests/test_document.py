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
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    assert output.exists(), "Output file was not created"
    group.remove_track(track)
    assert len(group.tracks) == 0, "Group should have no tracks after removal"
    doc.remove_group(group)
    assert len(doc.groups) == 0, "Document should have no groups after removal"


def test_basic_errors():
    doc = Document()
    group = Group("Group")
    track = Track("Track")

    with pytest.raises(TypeError, match="Expected a Group instance"):
        doc.add_group("dummy")
    with pytest.raises(TypeError, match="Expected a Track instance"):
        group.add_track("dummy")
    with pytest.raises(ValueError, match="Group not found in document"):
        doc.remove_group(group)
    with pytest.raises(ValueError, match="Track not found in group"):
        group.remove_track(track)
    doc.add_group(group)
    with pytest.raises(ValueError, match="Group already exists in document"):
        doc.add_group(group)
    group.add_track(track)
    with pytest.raises(ValueError, match="Track already exists in group"):
        group.add_track(track)
