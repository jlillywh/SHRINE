#!/usr/bin/env python3
"""Export a scenario run to CSV + JSON manifest (roadmap 3.13).

Example:
  .venv/bin/python3 examples/export_run_results.py scenarios/baseline_watershed.json ./my_run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from hydrology.watershed import Watershed  # noqa: E402
from shrine.simulation import Model, WatershedElement, export_run_result, load_and_run  # noqa: E402


def build_baseline_model() -> Model:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    model = Model(name="BaselineBasin")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a scenario and export CSV + JSON manifest")
    parser.add_argument(
        "scenario",
        type=Path,
        nargs="?",
        default=REPO_ROOT / "scenarios" / "baseline_watershed.json",
        help="Scenario YAML/JSON path",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        nargs="?",
        default=Path("run_export"),
        help="Directory for results.csv and run_manifest.json",
    )
    args = parser.parse_args()

    result = load_and_run(build_baseline_model, args.scenario)
    if not result.success:
        raise SystemExit(result.error)

    csv_path, manifest_path = export_run_result(result, args.output_dir)
    print(f"Wrote {csv_path}")
    print(f"Wrote {manifest_path}")
    print(f"rows={len(result.outputs)} scenario={result.manifest.get('scenario_name')}")


if __name__ == "__main__":
    main()
