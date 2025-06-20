from pathlib import Path

from partielspy import *

root = Path(__file__).parent.parent

template_in = root / "templates" / "factory.ptldoc"
template_out = root / "examples" / "templates" / "factory.ptldoc"
doc = Document.load(template_in)

group = doc.groups[0]
group.name = "Modified Group Name"

Path(template_out).parent.mkdir(parents=True, exist_ok=True)
doc.save(template_out)
