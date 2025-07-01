from pathlib import Path

from PIL import Image

from partielspy import *

root = Path(__file__).parent.parent
audio_file = root / "resource" / "Sound.wav"
template_file = root / "templates" / "factory.ptldoc"
output_folder = root / "examples" / "exports" / "JPEG"

document = Document.load(template_file)
Partiels().export(audio_file, document, output_folder, ExportConfigImage())
exported_image_spectrogram_path = output_folder / "Sound Group 1_Spectrogram.jpeg"
image = Image.open(exported_image_spectrogram_path)
image.show()
