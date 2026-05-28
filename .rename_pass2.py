import re
from pathlib import Path

ROOT = Path("/home/jason/ShrineObject")
EXTS = {".py", ".md", ".toml", ".yml", ".yaml", ".json", ".sh", ".txt"}
SKIP = {".git", ".venv", "venv", ".rename-sed.sh", ".rename_do.py"}

EXTRA = [
    ("from shrine import", "from shrine import"),
    ("import ShrineObject", "import ShrineObject"),
    ("from global_attributes.shrine_object import ShrineObject", "from global_attributes.shrine_object import ShrineObject"),
    ("SHRINE_VERSION", "SHRINE_VERSION"),
    (" ShrineObject(", " ShrineObject("),
    ("= ShrineObject(", "= ShrineObject("),
    ("| `ShrineObject` |", "| `ShrineObject` |"),
    ("**SHRINE is", "**SHRINE is"),
    ("for SHRINE", "for SHRINE"),
    ("evaluating SHRINE", "evaluating SHRINE"),
    ("installs `shrine*`", "installs `shrine*`"),
    ("Fix `ShrineObject.get_instance_count()`", "Fix `ShrineObject.get_instance_count()`"),
    ("coverage ?80% on `shrine`", "coverage ?80% on `shrine`"),
    ("trust SHRINE in", "trust SHRINE in"),
    ("how SHRINE differs", "how SHRINE differs"),
    ("`shrine-wrm`", "`shrine-wrm`"),
    ("`shrine-water`", "`shrine-water`"),
    ("pip install shrine[", "pip install shrine["),
    ("?SHRINE water", "?SHRINE water"),
    ("extend SHRINE without", "extend SHRINE without"),
    ("`shrine.elements`", "`shrine.elements`"),
    ("`shrine-element-cookiecutter`", "`shrine-element-cookiecutter`"),
    ("| `pip install shrine`", "| `pip install shrine`"),
    ("**SHRINE simulation framework**", "**SHRINE simulation framework**"),
    ("The SHRINE simulation framework", "The SHRINE simulation framework"),
    ("lives under `shrine`", "lives under `shrine`"),
    ("found in SHRINE", "found in SHRINE"),
    ("used by SHRINE core", "used by SHRINE core"),
    ("Run SHRINE simulation", "Run SHRINE simulation"),
    ("scripts for SHRINE", "scripts for SHRINE"),
    ("cd /home/jason/SHRINE", "cd /home/jason/SHRINE"),
]

n = 0
for path in ROOT.rglob("*"):
    if not path.is_file() or path.name in SKIP:
        continue
    if any(p in SKIP for p in path.parts):
        continue
    if path.suffix not in EXTS:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    orig = text
    for old, new in EXTRA:
        text = text.replace(old, new)
    if path.suffix == ".py" and "ShrineObject" in text:
        # remaining identifier uses in Python (not in strings we skip lightly)
        text = re.sub(r"\bAegis\b", "ShrineObject", text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        n += 1
print(f"PASS2 files={n}")
