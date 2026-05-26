"""Domain adapters for the simulation framework."""

from aegis.simulation.adapters.reservoir import ReservoirElement, StorageLike
from aegis.simulation.adapters.watershed import WatershedElement

__all__ = ["ReservoirElement", "StorageLike", "WatershedElement"]
