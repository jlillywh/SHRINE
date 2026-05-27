#!/usr/bin/env python3
"""Example: two catchments → junction → sink with flow solve and mass balance."""

from __future__ import annotations

from shrine.simulation import (
    Clock,
    ConstantInput,
    InputManager,
    Model,
    RunController,
    WatershedElement,
)
from hydrology.watershed import Watershed


def build_watershed() -> Watershed:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    ws.link_catchment("C2", "J1")
    return ws


def main() -> None:
    clock = Clock("1/1/2019", "1/15/2019")
    model = Model(name="TwinCatchment", clock=clock)
    model.register_watershed(
        "basin",
        WatershedElement(build_watershed(), element_id="basin"),
    )

    inputs = InputManager()
    inputs.bind("precipitation", ConstantInput(10.0))
    inputs.bind("evaporation", ConstantInput(1.0))

    result = RunController(model, input_manager=inputs).run()
    print(result.metadata)
    print(result.outputs[["basin.outflow", "basin.total_supply"]].head())


if __name__ == "__main__":
    main()
