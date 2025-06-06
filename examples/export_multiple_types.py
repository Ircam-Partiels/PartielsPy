from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent
audio_file = root / "resource" / "Sound.wav"
template_file = root / "templates" / "factory.ptldoc"
output_folder = root / "examples" / "exports" / "multiple"

partiels = Partiels()
partiels.export(audio_file, template_file, output_folder, ExportConfigImage())
partiels.export(audio_file, template_file, output_folder, ExportConfigCsv())
partiels.export(audio_file, template_file, output_folder, ExportConfigJson())
