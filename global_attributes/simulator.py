"""Removed legacy Simulator prototype (1.6).

The original ``Simulator`` referenced undefined attributes (``self.r``, ``self.w``)
and was replaced by :class:`shrine.simulation.RunController`.

Do not restore the old implementation. Use::

    from shrine.simulation import RunController, Model

See ``examples/climate_loop.py`` and ``docs/step-debugging.md``.
"""

from __future__ import annotations

import warnings

_DEPRECATION = (
    "global_attributes.Simulator was removed; use shrine.simulation.RunController "
    "(see examples/climate_loop.py)."
)


class Simulator:
    """Deprecated placeholder — the legacy prototype has been removed."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        warnings.warn(_DEPRECATION, DeprecationWarning, stacklevel=2)
        raise NotImplementedError(_DEPRECATION)

    def run(self, *args: object, **kwargs: object) -> None:
        warnings.warn(_DEPRECATION, DeprecationWarning, stacklevel=2)
        raise NotImplementedError(_DEPRECATION)
