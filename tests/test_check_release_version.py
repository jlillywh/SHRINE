"""Tests for scripts/check_release_version.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_release_version.py"


def test_check_release_version_matches_v0_2_0() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--tag", "v0.2.0"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "OK" in result.stdout


def test_check_release_version_rejects_mismatch() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--tag", "v9.9.9"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "ERROR" in result.stderr
