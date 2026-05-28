"""Adapter: :class:`~water_manage.store.Store` / Reservoir → Simulatable."""

from __future__ import annotations

from typing import Any, Protocol

from shrine.simulation.balance import MassBalanceTerm
from shrine.simulation.context import RunContext, TimestepContext


class StorageLike(Protocol):
    """Minimal storage interface for the reservoir adapter."""

    inflow: float
    request: float
    outflow: float
    overflow: float

    @property
    def quantity(self) -> float: ...

    def update(self) -> None: ...


class ReservoirElement:
    """Storage element with optional inflow/release inputs and mass balance."""

    element_type = "reservoir"

    def __init__(
        self,
        store: StorageLike,
        *,
        element_id: str = "reservoir",
        inflow_key: str = "inflow",
        release_key: str | None = "release",
        default_release: float = 0.0,
    ) -> None:
        self.store = store
        self.element_id = element_id
        self.inflow_key = inflow_key
        self.release_key = release_key
        self.default_release = default_release
        self._volume_before = 0.0
        self._last_inflow = 0.0
        self._last_outflow = 0.0
        self._last_overflow = 0.0

    def initialize(self, run_context: RunContext) -> None:
        recorder = run_context.recorder
        if recorder is not None:
            recorder.register(f"{self.element_id}.storage")
            recorder.register(f"{self.element_id}.outflow")

    def update(self, timestep_context: TimestepContext) -> None:
        self._volume_before = float(self.store.quantity)
        self._last_inflow = float(timestep_context.inputs.get(self.inflow_key, 0.0))
        release = self.default_release
        if self.release_key is not None:
            release = float(timestep_context.inputs.get(self.release_key, release))

        self.store.inflow = self._last_inflow
        self.store.request = release
        self.store.update()
        self._last_outflow = float(self.store.outflow)
        self._last_overflow = float(self.store.overflow)

        recorder = timestep_context.recorder
        if recorder is not None:
            recorder.record(f"{self.element_id}.storage", self.store.quantity)
            recorder.record(f"{self.element_id}.outflow", self._last_outflow)

    def balance_terms(self, timestep_context: TimestepContext) -> list[MassBalanceTerm]:
        """inflow − outflow − overflow − Δstorage ≈ 0."""
        delta_storage = float(self.store.quantity) - self._volume_before
        prefix = self.element_id
        return [
            MassBalanceTerm(f"{prefix}.inflow", self._last_inflow),
            MassBalanceTerm(f"{prefix}.outflow", -self._last_outflow),
            MassBalanceTerm(f"{prefix}.overflow", -self._last_overflow),
            MassBalanceTerm(f"{prefix}.storage_delta", -delta_storage),
        ]

    def finalize(self, run_context: RunContext) -> None:
        pass
