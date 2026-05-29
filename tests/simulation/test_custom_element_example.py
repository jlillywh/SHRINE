"""Smoke test for examples/custom_element.py (extension guide)."""

from __future__ import annotations

from examples.custom_element import DemandElement

from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController


def test_demand_element_records_input() -> None:
    model = Model(clock=Clock("1/1/2019", "1/4/2019"))
    model.register("d1", DemandElement("d1"))
    inputs = InputManager()
    inputs.bind("demand", ConstantInput(4.0))
    result = RunController(model, input_manager=inputs, raise_on_error=False).run()
    assert result.success
    assert result.outputs["d1.applied"].iloc[0] == 4.0
    assert len(result.outputs) == 4
