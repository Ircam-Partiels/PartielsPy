from pathlib import Path

from PIL import Image

from partielspy import *

root = Path(__file__).parent.parent
template_file = root / "templates" / "factory.ptldoc"
output_folder = root / "examples" / "exports" / "JPEG"

document = Document(
    document_file=template_file, audio_file_layout=root / "resource" / "Sound.wav"
)
Partiels().export(
    document, output_folder, ExportConfig(format=ExportConfig.Formats.JPEG)
)
exported_image_spectrogram_path = output_folder / "Group 1_Spectrogram.jpeg"
image = Image.open(exported_image_spectrogram_path)
image.show()
