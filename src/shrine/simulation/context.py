"""Run and timestep context objects passed to elements."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd

from shrine.simulation.clock import Clock
from shrine.simulation.rng import make_rng

if TYPE_CHECKING:
    from pint import UnitRegistry

    from shrine.simulation.recorder import Recorder


@dataclass
class RunContext:
    """Context for an entire run."""

    model_id: str
    clock: Clock
    scenario_name: str | None = None
    seed: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    recorder: Recorder | None = None
    rng: np.random.Generator | None = None
    units_registry: UnitRegistry | None = None
    default_units: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if self.rng is None:
            object.__setattr__(self, "rng", make_rng(self.seed))
        if self.units_registry is None or self.default_units is None:
            from shrine.units import get_default_units, get_unit_registry

            if self.units_registry is None:
                object.__setattr__(self, "units_registry", get_unit_registry())
            if self.default_units is None:
                object.__setattr__(self, "default_units", get_default_units())


@dataclass
class TimestepContext:
    """Context for a single timestep."""

    run: RunContext
    step_index: int
    current_time: pd.Timestamp
    dt: pd.Timedelta
    inputs: dict[str, Any] = field(default_factory=dict)

    @property
    def clock(self) -> Clock:
        return self.run.clock

    @property
    def recorder(self) -> Recorder | None:
        return self.run.recorder

    @property
    def rng(self) -> np.random.Generator:
        return self.run.rng

    @property
    def units_registry(self) -> UnitRegistry:
        return self.run.units_registry

    @property
    def default_units(self) -> dict[str, str]:
        return self.run.default_units
