"""Tests for shrine.source.Source."""

from __future__ import annotations

from shrine.source import Source


def test_source_total_outflow() -> None:
    source = Source("main", [("a", 1.5), ("b", 2.5)])
    assert source.name == "main"
    assert source.total_outflow() == 4.0


def test_source_outflow_by_name() -> None:
    source = Source("main", [("a", 1.0), ("b", 2.0)])
    assert source.outflow_by_name("a") == 1.0
    assert source.outflow_by_name("missing") == 0.0
