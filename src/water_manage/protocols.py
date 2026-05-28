"""Typed contracts for water management domain modules (Phase 2)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class StorageElement(Protocol):
    """Mass-balance storage backend for reservoirs and simulation adapters.

    Satisfied by :class:`~water_manage.store.Store`, :class:`~water_manage.reservoir.Reservoir`,
    and test doubles such as :class:`~tests.conftest.SimpleStore`.

    Timestep contract (used by :class:`~shrine.simulation.adapters.reservoir.ReservoirElement`):

    1. Assign ``inflow`` and ``request`` for the step.
    2. Call ``update()`` with no arguments (implementations may also accept optional
       ``inflow`` / ``request`` keyword arguments).
    3. Read ``quantity``, ``outflow``, and ``overflow`` after ``update()``.

    Scenario overrides may set ``capacity`` and ``quantity`` when the implementation
    exposes those properties (see ``STORAGE_OVERRIDE_KEYS`` in the reservoir adapter).
    """

    inflow: float
    request: float
    outflow: float
    overflow: float

    @property
    def quantity(self) -> float: ...

    @quantity.setter
    def quantity(self, value: float) -> None: ...

    @property
    def capacity(self) -> float: ...

    @capacity.setter
    def capacity(self, value: float) -> None: ...

    def update(self) -> None: ...


def as_storage_element(store: object) -> StorageElement:
    """Return *store* if it satisfies :class:`StorageElement`, else raise ``TypeError``."""
    if isinstance(store, StorageElement):
        return store
    raise TypeError(
        f"Object {store!r} does not implement StorageElement "
        "(required: inflow, request, outflow, overflow, quantity, capacity, update)"
    )
