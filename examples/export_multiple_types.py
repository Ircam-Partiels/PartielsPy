from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent
template_file = root / "templates" / "factory.ptldoc"
output_folder = root / "examples" / "exports" / "multiple"

partiels = Partiels()
document = Document(document_file=template_file)
document.audio_file_layout = root / "resource" / "Sound.wav"
partiels.export(document, output_folder, ExportConfig(format=ExportConfig.Formats.JPEG))
partiels.export(document, output_folder, ExportConfig(format=ExportConfig.Formats.CSV))
partiels.export(document, output_folder, ExportConfig(format=ExportConfig.Formats.JSON))
