"""Single-timestep debugging API (RUN-04)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from shrine.simulation.balance import MassBalanceReport
from shrine.simulation.context import TimestepContext


@dataclass(frozen=True)
class StepResult:
    """Outcome of one ``RunController.step()`` call."""

    step_index: int
    current_time: pd.Timestamp
    inputs: dict[str, Any]
    timestep_context: TimestepContext
    balance: MassBalanceReport | None = None
    done: bool = False

    @property
    def passed(self) -> bool:
        """Whether mass balance passed (or was not checked)."""
        return self.balance is None or self.balance.passed
