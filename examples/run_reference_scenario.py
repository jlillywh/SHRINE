#!/usr/bin/env python3
"""Run a bundled reference scenario by stem name (roadmap 3.10).

Example:
  .venv/bin/python3 examples/run_reference_scenario.py synthetic_twin_catchment
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tests.reference.manifest import REFERENCE_CASES  # noqa: E402

from shrine.simulation import load_and_run  # noqa: E402


def _lookup(stem: str):
    for case in REFERENCE_CASES:
        if Path(case.scenario).stem == stem:
            return case
    names = ", ".join(Path(c.scenario).stem for c in REFERENCE_CASES)
    raise SystemExit(f"Unknown reference {stem!r}. Choose from: {names}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a scenarios/reference/ case")
    parser.add_argument(
        "reference",
        nargs="?",
        default="synthetic_twin_catchment",
        help="Scenario stem (filename without .yaml)",
    )
    args = parser.parse_args()
    case = _lookup(args.reference)
    scenario_path = REPO_ROOT / case.scenario
    result = load_and_run(case.builder, scenario_path)
    print(f"status={result.metadata.get('status')} scenario={result.metadata.get('scenario_name')}")
    if not result.success:
        raise SystemExit(result.error)
    print(result.outputs.head())
    print(f"… {len(result.outputs)} timesteps")


if __name__ == "__main__":
    main()
