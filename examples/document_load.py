from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent

template_in = root / "templates" / "factory.ptldoc"
template_out = root / "examples" / "templates" / "factory.ptldoc"
with open(template_in, "rb") as file:
    doc = Document.load(file.read())
print(doc.to_json())

group = doc.groups[0]
group.name = "Modified Group Name"
with open(template_out, "wb") as file:
    doc.save(file)
