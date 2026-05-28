from pathlib import Path
root = Path("/home/jason/Aegis")
readme = (root / "README.md").read_text(encoding="utf-8")
readme = readme.replace("# Aegis ? SHRINE (rename in progress)\n", "# SHRINE\n\n")
readme = readme.replace("Aegis combines", "SHRINE combines")
readme = readme.replace("shrine.simulation", "shrine.simulation")
readme = readme.replace("`shrine/simulation/`", "`shrine/simulation/`")
readme = readme.replace("cd Aegis", "cd <repo-root>")
readme = readme.replace("from shrine.simulation", "from shrine.simulation")
(root / "README.md").write_text(readme, encoding="utf-8")
pp = root / "pyproject.toml"
t = pp.read_text(encoding="utf-8")
import re
t = re.sub(
    r'^description = .*',
    'description = "SHRINE ? Simulation of Hydrology, Reservoirs, and Integrated Network Engine"',
    t,
    count=1,
    flags=re.M,
)
pp.write_text(t, encoding="utf-8")
pn = root / "docs/project-name.md"
if pn.exists():
    text = pn.read_text(encoding="utf-8")
    text = text.replace(
        "Code and folders may still use `aegis` until the migration in [modernization-roadmap.md](modernization-roadmap.md) is executed. New documentation should use **SHRINE** and the full name above.",
        "Python package layout uses `shrine` and `shrine.simulation`; see [modernization-roadmap.md](modernization-roadmap.md).",
    )
    pn.write_text(text, encoding="utf-8")
print("ok")
