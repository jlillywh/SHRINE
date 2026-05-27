#!/usr/bin/env python3
"""Minimal custom element example — see docs/extending-elements.md."""

from __future__ import annotations

from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController
from shrine.simulation.context import RunContext, TimestepContext


class DemandElement:
    """Applies a demand from bound inputs and records it each timestep."""

    element_type = "demand"

    def __init__(self, element_id: str = "demand") -> None:
        self.element_id = element_id
        self.applied = 0.0

    def initialize(self, run_context: RunContext) -> None:
        if run_context.recorder is not None:
            run_context.recorder.register(f"{self.element_id}.applied")

    def update(self, timestep_context: TimestepContext) -> None:
        self.applied = float(timestep_context.inputs.get("demand", 0.0))
        if timestep_context.recorder is not None:
            timestep_context.recorder.record(f"{self.element_id}.applied", self.applied)

    def finalize(self, run_context: RunContext) -> None:
        pass


def main() -> None:
    model = Model(name="DemandDemo", clock=Clock("1/1/2019", "1/6/2019"))
    model.register("d1", DemandElement("d1"))

    inputs = InputManager()
    inputs.bind("demand", ConstantInput(3.5))

    result = RunController(model, input_manager=inputs).run()
    print(result.outputs)


if __name__ == "__main__":
    main()
