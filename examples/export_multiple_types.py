from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent
audio_file = root / "resource" / "Sound.wav"
template_file = root / "templates" / "factory.ptldoc"
output_folder = root / "examples" / "exports" / "multiple"

partiels = Partiels()
document = Document.load(template_file)
partiels.export(
    audio_file, document, output_folder, ExportConfig(format=ExportConfig.Formats.JPEG)
)
partiels.export(
    audio_file, document, output_folder, ExportConfig(format=ExportConfig.Formats.CSV)
)
partiels.export(
    audio_file, document, output_folder, ExportConfig(format=ExportConfig.Formats.JSON)
)
