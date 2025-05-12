import pkg_resources

from PartielsPy.Partiels import Partiels


def test_create_instance():
    partiels = Partiels()
    print(partiels.getExecPath())
    assert partiels.getExecPath() is not None, "Partiels Executable not find"


def test_check_version():
    partiels = Partiels()
    assert (
        partiels.isHandledVersion is True
    ), "Partiels Executable Version does not match the wrapper"


def exports(partiels, document, dest):
    jpeg_exporter = partiels.createJpegExporter()
    assert jpeg_exporter.export(document, dest) == 0, "Export JPEG FAILED"

    png_exporter = partiels.createPngExporter()
    assert png_exporter.export(document, dest) == 0, "Export PNG FAILED"

    json_exporter = partiels.createJsonExporter()
    assert json_exporter.export(document, dest) == 0, "Export JSON FAILED"

    csv_exporter = partiels.createCsvExporter()
    assert csv_exporter.export(document, dest) == 0, "Export CSV FAILED"

    lab_exporter = partiels.createLabExporter()
    assert lab_exporter.export(document, dest) == 0, "Export LAB FAILED"

    cue_exporter = partiels.createCueExporter()
    assert cue_exporter.export(document, dest) != 0, "Export CUE SUCCESS"
    reaper_exporter = partiels.createReaperExporter()
    assert reaper_exporter.export(document, dest) != 0, "Export REAPER SUCCESS"

    sdif_exporter = partiels.createSdifExporter()
    err = sdif_exporter.export(document, dest)
    assert err == 0, "Export SDIF FAILED. ERROR CODE:" + str(err)


def test_export():
    partiels = Partiels()
    root = pkg_resources.resource_filename(__name__, "./")
    audiofile = root + "samples/Sound.wav"
    dest = root + "exports/"
    document = partiels.createDefaultDocument(audiofile, "factory")
    exports(partiels, document, dest)
    document = partiels.createDefaultDocument(audiofile, "supervp")
    exports(partiels, document, dest)
    document = partiels.createDefaultDocument(audiofile, "partials")
    exports(partiels, document, dest)
