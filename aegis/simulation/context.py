"""Run and timestep context objects passed to elements."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import pandas as pd

from aegis.simulation.clock import Clock

if TYPE_CHECKING:
    from aegis.simulation.recorder import Recorder


@dataclass
class RunContext:
    """Context for an entire run."""

    model_id: str
    clock: Clock
    scenario_name: str | None = None
    seed: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    recorder: Recorder | None = None


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
