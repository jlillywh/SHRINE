"""Built-in simulation elements for examples and tests."""

from __future__ import annotations

from aegis.simulation.context import RunContext, TimestepContext


class ClimateRecorderElement:
    """Records bound ``evaporation`` and ``precipitation`` inputs each timestep."""

    element_type = "climate_recorder"

    def __init__(
        self,
        *,
        evaporation_key: str = "evaporation",
        precipitation_key: str = "precipitation",
    ) -> None:
        self.evaporation_key = evaporation_key
        self.precipitation_key = precipitation_key

    def initialize(self, run_context: RunContext) -> None:
        recorder = run_context.recorder
        if recorder is not None:
            recorder.register("evaporation", unit="in")
            recorder.register("precipitation", unit="in")

    def update(self, timestep_context: TimestepContext) -> None:
        recorder = timestep_context.recorder
        if recorder is None:
            return
        recorder.record(
            "evaporation",
            timestep_context.inputs[self.evaporation_key],
        )
        recorder.record(
            "precipitation",
            timestep_context.inputs[self.precipitation_key],
        )

    def finalize(self, run_context: RunContext) -> None:
        pass
