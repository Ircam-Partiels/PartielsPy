import os
import csv
from pathlib import Path

from partielspy import *

audio_file = "path/to/audiofile.wav"
template_file = "path/to/template.xml"
output_folder = "path/to/output"

try:
    Partiels().export(audio_file, template_file, output_folder, ExportConfigCsv())
    exported_csvs = os.listdir(output_folder)
    for exported_csv in exported_csvs:
        csv_path = output_folder / exported_csv
        with open(csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                print(line)

except Partiels.ExportError as e:
    print(e.stderr)
