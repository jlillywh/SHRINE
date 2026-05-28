"""Repo-relative paths for legacy domain tests (importable without pytest)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
