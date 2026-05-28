#!/usr/bin/env python3
"""Example: standalone catchment with rational runoff (no flow network)."""

from __future__ import annotations

from shrine.simulation import (
    CatchmentElement,
    Clock,
    ConstantInput,
    InputManager,
    Model,
    RunController,
)


def main() -> None:
    clock = Clock("1/1/2019", "1/8/2019")
    model = Model(name="RationalCatchment", clock=clock)
    model.register_catchment(
        "hillslope",
        CatchmentElement(element_id="hillslope", area=5000.0, runoff_method="simple"),
    )

    inputs = InputManager()
    inputs.bind("precipitation", ConstantInput(10.0))
    inputs.bind("evaporation", ConstantInput(1.0))

    result = RunController(model, input_manager=inputs).run()
    print(result.metadata)
    print(result.outputs[["hillslope.outflow"]].head())


if __name__ == "__main__":
    main()
