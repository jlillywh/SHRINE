#!/usr/bin/env python3
"""Run a watershed model from a CSV-driven scenario (roadmap 3.14)."""

from __future__ import annotations

import argparse
from pathlib import Path

from hydrology.watershed import Watershed
from shrine.simulation import Model, WatershedElement, load_and_run


def build_model() -> Model:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    model = Model(name="CsvBasin")
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


def main() -> None:
    default = Path(__file__).resolve().parent.parent / "scenarios" / "csv_watershed.yaml"
    parser = argparse.ArgumentParser(description="Run SHRINE from a CSV climate scenario")
    parser.add_argument("scenario", type=Path, nargs="?", default=default)
    args = parser.parse_args()

    result = load_and_run(build_model, args.scenario)
    print(result.metadata)
    if result.success:
        print(result.outputs[["basin.outflow", "basin.total_supply"]].head())
    else:
        raise SystemExit(result.error)


if __name__ == "__main__":
    main()
