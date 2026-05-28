"""Domain adapters for the simulation framework."""

from shrine.simulation.adapters.reservoir import ReservoirElement, StorageLike
from shrine.simulation.adapters.watershed import WatershedElement

__all__ = ["ReservoirElement", "StorageLike", "WatershedElement"]
