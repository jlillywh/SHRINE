"""Run and timestep context objects passed to elements."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd

from shrine.simulation.clock import Clock
from shrine.simulation.rng import make_rng

if TYPE_CHECKING:
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

    def __post_init__(self) -> None:
        if self.rng is None:
            object.__setattr__(self, "rng", make_rng(self.seed))


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
