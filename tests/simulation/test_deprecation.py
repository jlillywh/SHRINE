"""Tests for API deprecation helpers."""

from __future__ import annotations

import pytest

from shrine.simulation import warn_api_deprecated


def test_warn_api_deprecated_message():
    with pytest.warns(DeprecationWarning, match="old_fn.*new_fn.*api-stability"):
        warn_api_deprecated("old_fn", replacement="new_fn", removed_in_api="2.0")
