"""{{ cookiecutter.element_class_name }} — a SHRINE Simulatable element plugin."""

from __future__ import annotations

from shrine.simulation.context import RunContext, TimestepContext


class {{ cookiecutter.element_class_name }}:
    """Reads ``{{ cookiecutter.input_key }}`` and records ``{{ cookiecutter.output_variable }}`` each timestep."""

    element_type = "{{ cookiecutter.element_type }}"

    def __init__(self, element_id: str = "{{ cookiecutter.entry_point_name }}") -> None:
        self.element_id = element_id
        self.{{ cookiecutter.output_variable }} = 0.0

    def initialize(self, run_context: RunContext) -> None:
        if run_context.recorder is not None:
            run_context.recorder.register(f"{self.element_id}.{{ cookiecutter.output_variable }}")

    def update(self, timestep_context: TimestepContext) -> None:
        self.{{ cookiecutter.output_variable }} = float(
            timestep_context.inputs.get("{{ cookiecutter.input_key }}", 0.0)
        )
        if timestep_context.recorder is not None:
            timestep_context.recorder.record(
                f"{self.element_id}.{{ cookiecutter.output_variable }}",
                self.{{ cookiecutter.output_variable }},
            )

    def finalize(self, run_context: RunContext) -> None:
        pass
