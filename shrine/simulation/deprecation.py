"""Deprecation helpers for the simulation public API."""

from __future__ import annotations

import warnings

from shrine.simulation.version import API_VERSION


def warn_api_deprecated(
    name: str,
    *,
    replacement: str | None = None,
    removed_in_api: str | None = None,
    stacklevel: int = 3,
) -> None:
    """Emit a standard :class:`DeprecationWarning` for a public API symbol.

    Parameters
    ----------
    name
        Deprecated symbol (e.g. ``"RunController.legacy_run"``).
    replacement
        Suggested replacement (e.g. ``"RunController.run"``).
    removed_in_api
        Planned ``shrine.simulation.__api_version__`` when the symbol is removed.
    stacklevel
        Passed to :func:`warnings.warn` (default targets caller's caller).
    """
    message = f"{name} is deprecated and will be removed in a future release."
    if replacement:
        message += f" Use {replacement} instead."
    if removed_in_api:
        message += (
            f" It will be removed when shrine.simulation.__api_version__ "
            f"reaches {removed_in_api} (current {API_VERSION})."
        )
    message += " See docs/api-stability.md."
    warnings.warn(message, DeprecationWarning, stacklevel=stacklevel)
