import csv
from pathlib import Path

from partielspy import ExportConfigCsv, Partiels

root = Path(__file__).parent.parent
audio_file = root / "resource" / "Sound.wav"
template_file = root / "templates" / "factory.ptldoc"
output_folder = root / "examples" / "exports" / "CSV"

partiels = Partiels()
config = ExportConfigCsv(include_header=True)
partiels.export(audio_file, template_file, output_folder, config)
exported_csv_waveform_path = output_folder / "Sound Group 2_Waveform.csv"
with open(exported_csv_waveform_path, newline="", encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    for line in reader:
        print(line)
