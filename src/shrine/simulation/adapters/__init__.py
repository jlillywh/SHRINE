"""Domain adapters for the simulation framework."""

from shrine.simulation.adapters.catchment import CatchmentElement
from shrine.simulation.adapters.reservoir import ReservoirElement, StorageLike
from water_manage.protocols import StorageElement
from shrine.simulation.adapters.watershed import WatershedElement

__all__ = [
    "CatchmentElement",
    "ReservoirElement",
    "StorageElement",
    "StorageLike",
    "WatershedElement",
]
