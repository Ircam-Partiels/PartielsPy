import os
from pathlib import Path

from PIL import Image

from partielspy import *

audio_file = "path/to/audiofile.wav"
template_file = "path/to/template.xml"
output_folder = "path/to/output"

try:
    Partiels().export(audio_file, template_file, output_folder, ExportConfigImage())
    exported_images = os.listdir(output_folder)
    for image in exported_images:
        image_path = output_folder / image
        img = Image.open(image_path)
        img.show()
except Partiels.ExportError as e:
    print(e.stderr)
