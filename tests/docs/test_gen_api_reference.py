"""Tests for API reference generation (roadmap 3.2)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTOGEN = ROOT / "docs" / "api" / "autogen"
GEN_SCRIPT = ROOT / "scripts" / "gen_api_reference.py"


def test_gen_api_reference_covers_public_api() -> None:
    result = subprocess.run(
        [sys.executable, str(GEN_SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Wrote 9 API pages" in result.stdout
    assert (AUTOGEN / "run-orchestration.md").is_file()
    assert (AUTOGEN / "inputs.md").is_file()

    import shrine.simulation as sim

    for name in sim.__all__:
        if name.startswith("__"):
            continue
        text = " ".join(p.read_text(encoding="utf-8") for p in AUTOGEN.glob("*.md") if p.name != "README.md")
        assert name in text, f"{name!r} missing from generated API pages"
