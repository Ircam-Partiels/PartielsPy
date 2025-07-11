import csv
from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent

template_file = root / "templates" / "factory.ptldoc"
output_folder = root / "examples" / "exports" / "CSV"

partiels = Partiels()
config = ExportConfig(format=ExportConfig.Formats.CSV, csv_include_header=True)
document = Document(
    document_file=template_file, audio_file_layout=root / "resource" / "Sound.wav"
)
partiels.export(document, output_folder, config)
exported_csv_waveform_path = output_folder / "Group 2_Waveform.csv"
with open(exported_csv_waveform_path, newline="", encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    for line in reader:
        print(line)
