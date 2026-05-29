#!/usr/bin/env python3
"""Refresh golden output hashes for scenarios/reference/ (roadmap 3.10)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tests.reference.manifest import REFERENCE_CASES  # noqa: E402

from shrine.simulation import load_scenario_file, run_scenario  # noqa: E402
from shrine.simulation.golden import outputs_content_hash  # noqa: E402

GOLDEN = REPO_ROOT / "tests" / "golden" / "reference"


def main() -> int:
    GOLDEN.mkdir(parents=True, exist_ok=True)
    for case in REFERENCE_CASES:
        path = REPO_ROOT / case.scenario
        scenario = load_scenario_file(path)
        result = run_scenario(case.builder(), scenario, raise_on_error=False)
        if not result.success:
            print(f"run failed for {path.name}: {result.error}", file=sys.stderr)
            return 1
        digest = outputs_content_hash(result.outputs)
        out = GOLDEN / case.golden
        out.write_text(digest + "\n", encoding="utf-8")
        print(f"{out.relative_to(REPO_ROOT)}  {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
