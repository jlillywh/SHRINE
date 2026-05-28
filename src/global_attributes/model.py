"""Legacy model shell.

Prefer :class:`shrine.simulation.Model` for new work (see ``examples/climate_loop.py``).
Excel / ``data_external`` loading was removed from :meth:`LegacyModel.__init__`; use simulation
inputs or an explicit script (``global_attributes/test_model.py`` is a legacy example only).
"""

from __future__ import annotations

import warnings

from global_attributes.shrine_object import ShrineObject
from global_attributes.clock import Clock
from global_attributes.set_label import SetLabel

_MODEL_ALIAS_DEPRECATION = (
    "global_attributes.Model is deprecated; use LegacyModel or "
    "shrine.simulation.Model instead (see examples/climate_loop.py)."
)

__all__ = ["LegacyModel", "Model"]


class LegacyModel(ShrineObject):
    """Legacy holder for a :class:`~global_attributes.clock.Clock` and label sets.

    Does not load files on construction. Former ``__init__`` side effects
    (``FileManager``, ``data.xlsx`` under ``data_external``) are intentionally removed.
    """

    def __init__(self) -> None:
        super().__init__()
        self.clock = Clock()
        self.listSet = SetLabel()


class Model(LegacyModel):
    """Deprecated alias for :class:`LegacyModel`."""

    def __init__(self) -> None:
        warnings.warn(_MODEL_ALIAS_DEPRECATION, DeprecationWarning, stacklevel=2)
        super().__init__()
