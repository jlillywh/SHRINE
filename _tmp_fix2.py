from pathlib import Path
import re
root = Path("/home/jason/Aegis")
p = root / "README.md"
t = p.read_text(encoding="utf-8")
t = re.sub(r"^# Aegis.*\n\n", "# SHRINE\n\n", t, count=1)
p.write_text(t, encoding="utf-8")
p = root / "pyproject.toml"
t = p.read_text(encoding="utf-8")
t = re.sub(
    r"^description = .*",
    'description = "SHRINE \u2014 Simulation of Hydrology, Reservoirs, and Integrated Network Engine"',
    t,
    count=1,
    flags=re.M,
)
p.write_text(t, encoding="utf-8")
print(p.read_text(encoding="utf-8").splitlines()[6])
