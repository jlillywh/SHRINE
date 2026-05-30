"""Verify the package registers a shrine.elements entry point."""

from __future__ import annotations

from shrine.simulation import create_element_from_plugin, list_element_plugins


def test_entry_point_is_listed() -> None:
    plugins = list_element_plugins()
    assert "{{ cookiecutter.entry_point_name }}" in plugins


def test_entry_point_loads_element() -> None:
    element = create_element_from_plugin("{{ cookiecutter.entry_point_name }}", element_id="d1")
    assert element.element_type == "{{ cookiecutter.element_type }}"
    assert element.element_id == "d1"
