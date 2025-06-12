from pathlib import Path

from partielspy import *

folder = Path(__file__).parent / "templates"

template_in = folder / "example.ptldoc"
template_out = folder / "example_out.ptldoc"
doc = Document(template_in)
print(doc)
group = doc.groups[0]
group.name = "Modified Group Name"
Partiels().document_to_xml(doc, template_out)
