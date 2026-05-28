"""Structured errors for simulation runs (RUN-06/07, D6)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SimulationPhase(str, Enum):
    """Phase of the timestep loop when a failure occurred."""

    VALIDATE = "validate"
    INITIALIZE = "initialize"
    INPUT = "input"
    UPDATE = "update"
    FLOW_SOLVE = "flow_solve"
    BALANCE = "balance"
    RECORD = "record"
    FINALIZE = "finalize"


@dataclass
class SimulationError(Exception):
    """Fail-fast simulation error with diagnostic context."""

    message: str
    phase: SimulationPhase
    element_id: str | None = None
    step_index: int | None = None
    timestamp: Any = None
    details: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        parts = [self.message, f"phase={self.phase.value}"]
        if self.element_id is not None:
            parts.append(f"element_id={self.element_id}")
        if self.step_index is not None:
            parts.append(f"step_index={self.step_index}")
        if self.timestamp is not None:
            parts.append(f"timestamp={self.timestamp}")
        return "; ".join(parts)
