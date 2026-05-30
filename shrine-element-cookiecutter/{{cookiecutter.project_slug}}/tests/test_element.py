"""Tests for {{ cookiecutter.element_class_name }}."""

from __future__ import annotations

from {{ cookiecutter.package_name }}.element import {{ cookiecutter.element_class_name }}

from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController


def test_element_records_input() -> None:
    model = Model(clock=Clock("1/1/2019", "1/4/2019"))
    model.register("d1", {{ cookiecutter.element_class_name }}("d1"))

    inputs = InputManager()
    inputs.bind("{{ cookiecutter.input_key }}", ConstantInput(2.5))

    result = RunController(model, input_manager=inputs, raise_on_error=False).run()
    assert result.success
    assert result.outputs["d1.{{ cookiecutter.output_variable }}"].iloc[0] == 2.5


def test_register_plugin_runs() -> None:
    model = Model(clock=Clock("1/1/2019", "1/4/2019"))
    model.register_plugin("d1", "{{ cookiecutter.entry_point_name }}", element_id="d1")

    inputs = InputManager()
    inputs.bind("{{ cookiecutter.input_key }}", ConstantInput(1.0))

    result = RunController(model, input_manager=inputs, raise_on_error=False).run()
    assert result.success
