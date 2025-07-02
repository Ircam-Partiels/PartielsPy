from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent
audio_file = root / "resource" / "Sound.wav"
template_file = root / "templates" / "factory.ptldoc"
output_folder = root / "examples" / "exports" / "multiple"

partiels = Partiels()
document = Document.load(template_file)
partiels.export(audio_file, document, output_folder, ExportConfigImage())
partiels.export(audio_file, document, output_folder, ExportConfigCsv())
partiels.export(audio_file, document, output_folder, ExportConfigJson())
