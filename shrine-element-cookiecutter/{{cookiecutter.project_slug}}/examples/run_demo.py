#!/usr/bin/env python3
"""Minimal demo run for {{ cookiecutter.project_name }}."""

from __future__ import annotations

from shrine.simulation import Clock, ConstantInput, InputManager, Model, RunController


def main() -> None:
    model = Model(name="{{ cookiecutter.project_name }}", clock=Clock("1/1/2019", "1/6/2019"))
    model.register_plugin("d1", "{{ cookiecutter.entry_point_name }}", element_id="d1")

    inputs = InputManager()
    inputs.bind("{{ cookiecutter.input_key }}", ConstantInput(3.5))

    result = RunController(model, input_manager=inputs).run()
    print(result.outputs)


if __name__ == "__main__":
    main()
