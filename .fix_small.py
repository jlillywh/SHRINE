from pathlib import Path
for rel, subs in [
    (".gitleaks.toml", [("SHRINE gitleaks", "SHRINE gitleaks")]),
    ("docs/modernization-roadmap.md", [
        ("on `aegis`", "on `shrine`"),
        ("?Aegis water", "?SHRINE water"),
    ]),
]:
    p = Path("/home/jason/Aegis") / rel
    t = p.read_text(encoding="utf-8")
    for a, b in subs:
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8")
print("fixed")
