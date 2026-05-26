"""Simulation element protocol (ELM-01)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from aegis.simulation.context import RunContext, TimestepContext


@runtime_checkable
class Simulatable(Protocol):
    """Contract for elements executed by the simulation framework."""

    @property
    def element_type(self) -> str:
        """Short type label (e.g. 'watershed', 'reservoir')."""
        ...

    def initialize(self, run_context: RunContext) -> None:
        """Prepare element state before the first timestep."""
        ...

    def update(self, timestep_context: TimestepContext) -> None:
        """Advance element state for the current timestep."""
        ...

    def finalize(self, run_context: RunContext) -> None:
        """Optional post-run hook."""
        ...
