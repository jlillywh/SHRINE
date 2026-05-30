#!/usr/bin/env python3
"""Verify release tag matches pyproject.toml and shrine.__version__ (roadmap 3.6)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read_pyproject_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise SystemExit("Could not find [project] version in pyproject.toml")
    return match.group(1)


def _read_init_version() -> str:
    text = (ROOT / "src" / "shrine" / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise SystemExit("Could not find __version__ in src/shrine/__init__.py")
    return match.group(1)


def _normalize_tag(tag: str) -> str:
    return tag[1:] if tag.startswith("v") else tag


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="Git tag (e.g. v0.2.0)")
    args = parser.parse_args()

    expected = _normalize_tag(args.tag)
    pyproject_version = _read_pyproject_version()
    init_version = _read_init_version()

    errors: list[str] = []
    if pyproject_version != expected:
        errors.append(f"pyproject.toml version {pyproject_version!r} != tag {expected!r}")
    if init_version != expected:
        errors.append(f"shrine.__version__ {init_version!r} != tag {expected!r}")
    if pyproject_version != init_version:
        errors.append(f"pyproject.toml ({pyproject_version!r}) != __init__.py ({init_version!r})")

    if errors:
        for message in errors:
            print(f"ERROR: {message}", file=sys.stderr)
        raise SystemExit(1)

    print(f"OK: release tag v{expected} matches package version")


if __name__ == "__main__":
    main()
