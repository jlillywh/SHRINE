#!/usr/bin/env python3
"""Add ``from __future__ import annotations`` to domain modules missing it (roadmap 2.13)."""

from __future__ import annotations

from pathlib import Path

PACKAGES = (
    "hydrology",
    "water_manage",
    "geometry",
    "inputs",
    "data",
    "results",
    "hydraulics",
    "numerical",
    "controllers",
    "utils",
    "global_attributes",
    "testing",
)
MARKER = "from __future__ import annotations"
FUTURE_LINE = "from __future__ import annotations\n"


def _insert_index(lines: list[str]) -> int:
    index = 0
    if lines and lines[0].startswith("#!"):
        index = 1
    if index >= len(lines):
        return index
    stripped = lines[index].lstrip()
    if not (stripped.startswith('"""') or stripped.startswith("'''")):
        return index
    quote = stripped[:3]
    if stripped.count(quote) >= 2 and stripped.rstrip().endswith(quote):
        return index + 1
    for offset in range(index + 1, len(lines)):
        if quote in lines[offset]:
            return offset + 1
    return index + 1


def add_future_import(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    lines = text.splitlines(keepends=True)
    insert_at = _insert_index(lines)
    prefix = lines[:insert_at]
    suffix = lines[insert_at:]
    if prefix and prefix[-1].strip():
        prefix.append("\n")
    prefix.append(FUTURE_LINE)
    if suffix and suffix[0].strip():
        prefix.append("\n")
    path.write_text("".join(prefix + suffix), encoding="utf-8")
    return True


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "src"
    updated: list[Path] = []
    for package in PACKAGES:
        package_root = root / package
        if not package_root.is_dir():
            continue
        for path in sorted(package_root.rglob("*.py")):
            if add_future_import(path):
                updated.append(path)
    print(f"Updated {len(updated)} files")
    for path in updated:
        print(path.relative_to(root.parent))


if __name__ == "__main__":
    main()
