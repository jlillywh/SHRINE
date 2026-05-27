"""Ensure the published ``shrine.simulation`` API is importable and stable."""

from __future__ import annotations

import shrine.simulation as simulation


def test_all_exports_are_defined():
    for name in simulation.__all__:
        assert hasattr(simulation, name), name


def test_api_version_is_semver_like():
    parts = simulation.__api_version__.split(".")
    assert len(parts) >= 2
    assert all(part.isdigit() for part in parts[:2])
