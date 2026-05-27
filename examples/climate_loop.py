#!/usr/bin/env python3
"""Climate input replay using the simulation framework.

Port of ``global_attributes/test_model.py`` without a hand-written clock loop.
Uses synthetic monthly evaporation and precipitation (no Excel required).
"""

from __future__ import annotations

from shrine.simulation import (
    Clock,
    ClimateRecorderElement,
    InputManager,
    Model,
    MonthlyLookupInput,
    RunController,
)
from results.time_history import TimeHistory

# Example monthly rates (inches/day), keyed by month name — same pattern as Vector + Months labels.
EVAPORATION_BY_MONTH = {
    "January": 0.02,
    "February": 0.03,
    "March": 0.05,
    "April": 0.08,
    "May": 0.12,
    "June": 0.15,
    "July": 0.16,
    "August": 0.14,
    "September": 0.10,
    "October": 0.06,
    "November": 0.04,
    "December": 0.02,
}

PRECIPITATION_BY_MONTH = {
    "January": 0.15,
    "February": 0.12,
    "March": 0.10,
    "April": 0.08,
    "May": 0.06,
    "June": 0.04,
    "July": 0.03,
    "August": 0.04,
    "September": 0.05,
    "October": 0.07,
    "November": 0.10,
    "December": 0.14,
}


def build_climate_model(
    start: str = "1/1/2019",
    end: str = "1/10/2019",
) -> tuple[Model, RunController]:
    clock = Clock(start, end, time_step="1 days")
    model = Model(name="ClimateReplay", clock=clock)
    model.register("climate", ClimateRecorderElement())

    inputs = InputManager()
    inputs.bind("evaporation", MonthlyLookupInput(EVAPORATION_BY_MONTH))
    inputs.bind("precipitation", MonthlyLookupInput(PRECIPITATION_BY_MONTH))

    controller = RunController(model, input_manager=inputs, raise_on_error=True)
    return model, controller


def main() -> None:
    _, controller = build_climate_model()
    result = controller.run()
    print(result.metadata)
    print(result.outputs.head())
    print(f"Recorded {len(result.outputs)} timesteps")

    history = TimeHistory.from_run_result(result, name="Climate Results", display_unit="in")
    assert len(history.series) == len(result.outputs)


if __name__ == "__main__":
    main()
