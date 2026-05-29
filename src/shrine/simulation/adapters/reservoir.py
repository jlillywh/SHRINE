"""Adapter: :class:`~water_manage.store.Store` / Reservoir → Simulatable."""

from __future__ import annotations

from typing import Any

from shrine.simulation.balance import MassBalanceTerm
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.errors import SimulationError, SimulationPhase
from water_manage.protocols import StorageElement

# Scenario ``overrides`` keys allowed for :class:`ReservoirElement` (SCN-01).
RESERVOIR_ELEMENT_OVERRIDE_KEYS = frozenset({"default_release", "inflow_key", "release_key"})
# Keys applied to the wrapped storage object (``element.store``).
STORAGE_OVERRIDE_KEYS = frozenset({"capacity", "quantity"})

# Shrine public alias; canonical protocol is :class:`water_manage.protocols.StorageElement`.
StorageLike = StorageElement


class ReservoirElement:
    """Storage element with optional inflow/release inputs and mass balance."""

    element_type = "reservoir"

    def __init__(
        self,
        store: StorageElement,
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


def apply_reservoir_element_override(
    element: ReservoirElement,
    key: str,
    value: Any,
) -> None:
    """Apply one scenario override to a reservoir element or its storage (validated keys)."""
    if key in RESERVOIR_ELEMENT_OVERRIDE_KEYS:
        setattr(element, key, value)
        return
    if key in STORAGE_OVERRIDE_KEYS:
        setattr(element.store, key, value)
        return
    allowed = sorted(RESERVOIR_ELEMENT_OVERRIDE_KEYS | STORAGE_OVERRIDE_KEYS)
    raise SimulationError(
        message=f"Unknown override {key!r} for reservoir element {element.element_id!r}; "
        f"allowed: {allowed}",
        phase=SimulationPhase.VALIDATE,
        element_id=element.element_id,
    )
