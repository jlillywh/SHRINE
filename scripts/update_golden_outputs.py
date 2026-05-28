#!/usr/bin/env python3
"""Refresh golden output hashes under tests/golden/."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from hydrology.watershed import Watershed  # noqa: E402
from shrine.simulation import (  # noqa: E402
    Clock,
    Model,
    WatershedElement,
    load_scenario_file,
    run_scenario,
)
from shrine.simulation.golden import outputs_content_hash  # noqa: E402

GOLDEN = REPO_ROOT / "tests" / "golden"
SCENARIOS = [
    ("baseline_watershed.json", "baseline_watershed.outputs.sha256"),
]


def _watershed_model() -> Model:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    model = Model(name="GoldenWatershed", clock=Clock("1/1/2019", "1/10/2019"))
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


def main() -> int:
    GOLDEN.mkdir(parents=True, exist_ok=True)
    for scenario_name, hash_name in SCENARIOS:
        path = REPO_ROOT / "scenarios" / scenario_name
        scenario = load_scenario_file(path)
        result = run_scenario(_watershed_model(), scenario, raise_on_error=False)
        if not result.success:
            print(f"run failed for {scenario_name}: {result.error}", file=sys.stderr)
            return 1
        digest = outputs_content_hash(result.outputs)
        out = GOLDEN / hash_name
        out.write_text(digest + "\n", encoding="utf-8")
        print(f"{out.relative_to(REPO_ROOT)}  {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
