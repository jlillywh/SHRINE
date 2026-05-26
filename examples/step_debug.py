#!/usr/bin/env python3
"""Interactive single-timestep debugging (RUN-04)."""

from __future__ import annotations

from aegis.simulation import (
    Clock,
    ConstantInput,
    InputManager,
    Model,
    RunController,
    WatershedElement,
)
from hydrology.watershed import Watershed


def main() -> None:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    model = Model(name="StepDebugBasin", clock=Clock("1/1/2019", "1/6/2019"))
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))

    inputs = InputManager()
    inputs.bind("precipitation", ConstantInput(10.0))
    inputs.bind("evaporation", ConstantInput(1.0))

    controller = RunController(model, input_manager=inputs, seed=1)
    controller.reset()

    while True:
        step = controller.step()
        if step is None:
            break
        residual = step.balance.residual if step.balance else 0.0
        outflow = step.timestep_context.inputs  # inputs visible on context
        print(
            f"t={step.current_time.date()} step={step.step_index} "
            f"balance_residual={residual:.6g} precip={outflow.get('precipitation')}"
        )

    result = controller.complete()
    print(result.metadata)
    print(result.outputs[["basin.outflow"]].head())


if __name__ == "__main__":
    main()
