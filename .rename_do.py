import os
import re
from pathlib import Path

ROOT = Path("/home/jason/Aegis")
EXTS = {".py", ".md", ".toml", ".yml", ".yaml", ".json", ".sh", ".txt"}
SKIP = {".git", ".venv", "venv"}

REPLACEMENTS = [
    ("shrine.simulation", "shrine.simulation"),
    ("from shrine.", "from shrine."),
    ("import shrine", "import shrine"),
    ("shrine/", "shrine/"),
    ("shrine_units", "shrine_units"),
    ("global_attributes.shrine_object", "global_attributes.shrine_object"),
    ("class ShrineObject", "class ShrineObject"),
    ("ShrineObject.__init__", "ShrineObject.__init__"),
    ("(ShrineObject)", "(ShrineObject)"),
    ("TestShrineObject", "TestShrineObject"),
    ("test_shrine_object", "test_shrine_object"),
    ('name = "shrine"', 'name = "shrine"'),
    ('include = ["shrine*', 'include = ["shrine*'),
    ('source = ["shrine"]', 'source = ["shrine"]'),
    ("# SHRINE", "# SHRINE"),
    ("SHRINE combines", "SHRINE combines"),
    ("Testing SHRINE", "Testing SHRINE"),
    ("SHRINE Simulation", "SHRINE Simulation"),
    ("Everything else in SHRINE", "Everything else in SHRINE"),
    ("the SHRINE simulation", "the SHRINE simulation"),
    ("A SHRINE ", "A SHRINE "),
    ("existing SHRINE class", "existing SHRINE class"),
    ("all SHRINE objects", "all SHRINE objects"),
    ("its SHRINE base_unit", "its SHRINE base_unit"),
    ("SHRINE object", "SHRINE object"),
    ("SHRINE objects", "SHRINE objects"),
    ("SHRINE TimeSeries", "SHRINE TimeSeries"),
    ("SHRINE", "SHRINE"),
    ("cd SHRINE", "cd SHRINE"),
    ("~/SHRINE", "~/SHRINE"),
    ('title = "SHRINE"', 'title = "SHRINE"'),
    ('"""SHRINE', '"""SHRINE'),
    ("global_attributes/shrine_object.py", "global_attributes/shrine_object.py"),
]

files_changed = 0
for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    if any(p in SKIP for p in path.parts):
        continue
    if path.suffix not in EXTS:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    orig = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        files_changed += 1

init = ROOT / "shrine" / "__init__.py"
if init.exists():
    lines = init.read_text(encoding="utf-8").splitlines()
    doc = '"""SHRINE ? Simulation of Hydrology, Reservoirs, and Integrated Network Engines."""'
    if lines:
        i = 0
        if lines[0].strip().startswith('"""') or lines[0].strip().startswith("'''"):
            lines[0] = doc
        else:
            lines.insert(0, doc)
        init.write_text("\n".join(lines) + "\n", encoding="utf-8")

sim_init = ROOT / "shrine" / "simulation" / "__init__.py"
if sim_init.exists():
    t = sim_init.read_text(encoding="utf-8")
    t2 = re.sub(r"(?m)^(\"\"\"|''').*?(aegis|Aegis).*?\1", '"""shrine.simulation ? simulation engine."""', t, count=1)
    if t2 == t:
        t2 = t.replace("shrine.simulation", "shrine.simulation").replace("Aegis", "SHRINE")
    sim_init.write_text(t2, encoding="utf-8")

print(f"PY_RENAME files_changed={files_changed}")
