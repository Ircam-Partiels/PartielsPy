import os

from PartielsPy.Partiels import Partiels


def test_create_default_document():
    """Test the creation of a Default Template Document"""
    partiels = Partiels()
    audiofile = "test.wav"
    template = "factory"
    document = partiels.createDefaultDocument(audiofile, template)
    assert document.audiofile is not None, "Audiofile path is not set correctly"
    assert document.template is not None, "Template path is not set correctly"
    assert os.path.isfile(document.template), "Template path is not a file"


def test_create_document():
    """Test the creation of a Document"""
    partiels = Partiels()
    audiofile = "test.wav"
    template = "test.ptldoc"
    document = partiels.createDocument(audiofile, template)
    assert document.audiofile is not None, "Audiofile path is not set correctly"
    assert document.template is not None, "Template path is not set correctly"
    document.setTemplate(template)
    assert document.audiofile is not None, "Audiofile path is not set correctly"
    assert document.template is not None, "Template path is not set correctly"
