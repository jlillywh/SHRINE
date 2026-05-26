#!/usr/bin/env python3
"""Run a watershed model from a scenario JSON or YAML file."""

from __future__ import annotations

import argparse
from pathlib import Path

from aegis.simulation import Model, WatershedElement, load_and_run
from hydrology.watershed import Watershed


def build_model() -> Model:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    model = Model(name="ScenarioBasin")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Aegis simulation from scenario file")
    parser.add_argument(
        "scenario",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parent.parent / "scenarios" / "baseline_watershed.json",
        help="Path to .json or .yaml scenario file",
    )
    args = parser.parse_args()

    result = load_and_run(build_model, args.scenario)
    print(result.metadata)
    if result.success:
        print(result.outputs[["basin.outflow", "basin.total_supply"]].head())
    else:
        raise SystemExit(result.error)


if __name__ == "__main__":
    main()
