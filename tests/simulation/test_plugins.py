"""Tests for ``shrine.elements`` plugin entry points (roadmap 4.1)."""

from __future__ import annotations

import importlib.metadata

import pytest

from shrine.simulation import (
    Clock,
    ConstantInput,
    InputManager,
    Model,
    RunController,
    Simulatable,
    create_element_from_plugin,
    list_element_plugins,
    load_element_plugin,
)
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.errors import SimulationError
from shrine.simulation.plugins import ELEMENTS_ENTRY_POINT_GROUP, clear_plugin_cache


class EchoElement:
    """Minimal plugin used by monkeypatched entry points in these tests."""

    element_type = "echo"

    def __init__(self, element_id: str = "echo", scale: float = 1.0) -> None:
        self.element_id = element_id
        self.scale = scale

    def initialize(self, run_context: RunContext) -> None:
        if run_context.recorder is not None:
            run_context.recorder.register(f"{self.element_id}.value")

    def update(self, timestep_context: TimestepContext) -> None:
        value = float(timestep_context.inputs.get("value", 0.0)) * self.scale
        if timestep_context.recorder is not None:
            timestep_context.recorder.record(f"{self.element_id}.value", value)

    def finalize(self, run_context: RunContext) -> None:
        pass


def echo_factory(*, element_id: str = "echo", scale: float = 1.0) -> EchoElement:
    return EchoElement(element_id=element_id, scale=scale)


def bad_factory() -> object:
    return object()


not_a_callable = 42


def broken_factory() -> EchoElement:
    raise ValueError("boom")


def _patch_entry_points(
    monkeypatch: pytest.MonkeyPatch,
    specs: list[tuple[str, str]],
) -> None:
    entry_points = importlib.metadata.EntryPoints(
        [
            importlib.metadata.EntryPoint(
                name=name,
                value=value,
                group=ELEMENTS_ENTRY_POINT_GROUP,
            )
            for name, value in specs
        ]
    )
    monkeypatch.setattr(
        "shrine.simulation.plugins._entry_points_for_group",
        lambda _group: entry_points,
    )
    clear_plugin_cache()


@pytest.fixture(autouse=True)
def _reset_plugin_cache() -> None:
    clear_plugin_cache()
    yield
    clear_plugin_cache()


def test_builtin_plugins_are_discovered() -> None:
    plugins = list_element_plugins()
    assert "watershed" in plugins
    assert "catchment" in plugins
    assert "reservoir" in plugins
    assert "climate_recorder" in plugins
    assert plugins["climate_recorder"].endswith("ClimateRecorderElement")


def test_load_builtin_plugin_target() -> None:
    plugin = load_element_plugin("climate_recorder")
    assert plugin.name == "climate_recorder"
    element = plugin.target()
    assert isinstance(element, Simulatable)


def test_create_element_from_plugin_runs() -> None:
    model = Model(clock=Clock("1/1/2019", "1/3/2019"))
    model.register_plugin("cr", "climate_recorder")

    inputs = InputManager()
    inputs.bind("evaporation", ConstantInput(0.1))
    inputs.bind("precipitation", ConstantInput(0.2))

    result = RunController(model, input_manager=inputs, raise_on_error=False).run()
    assert result.success
    assert "evaporation" in result.outputs


def test_unknown_plugin_raises() -> None:
    with pytest.raises(SimulationError, match="Unknown element plugin"):
        load_element_plugin("not_registered")


def test_unknown_plugin_with_no_plugins_lists_none(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_entry_points(monkeypatch, [])

    with pytest.raises(SimulationError, match="known plugins: \\(none\\)"):
        load_element_plugin("missing")


def test_broken_entry_point_load_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_entry_points(monkeypatch, [("broken", "no.such.module:MissingClass")])

    with pytest.raises(SimulationError, match="Failed to load element plugin"):
        load_element_plugin("broken")


def test_non_callable_plugin_target_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_entry_points(
        monkeypatch,
        [("static", "tests.simulation.test_plugins:not_a_callable")],
    )

    with pytest.raises(SimulationError, match="must resolve to a class or callable"):
        load_element_plugin("static")


def test_construction_failure_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_entry_points(
        monkeypatch,
        [("broken", "tests.simulation.test_plugins:broken_factory")],
    )

    with pytest.raises(SimulationError, match="Failed to construct element from plugin"):
        create_element_from_plugin("broken")


def test_monkeypatched_class_plugin(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_entry_points(
        monkeypatch,
        [("echo", "tests.simulation.test_plugins:EchoElement")],
    )

    element = create_element_from_plugin("echo", element_id="e1", scale=2.0)
    assert element.element_id == "e1"
    assert element.scale == 2.0


def test_monkeypatched_factory_plugin(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_entry_points(
        monkeypatch,
        [("echo", "tests.simulation.test_plugins:echo_factory")],
    )

    model = Model(clock=Clock("1/1/2019", "1/3/2019"))
    model.register_plugin("e1", "echo", element_id="e1", scale=3.0)

    inputs = InputManager()
    inputs.bind("value", ConstantInput(4.0))
    result = RunController(model, input_manager=inputs, raise_on_error=False).run()
    assert result.success
    assert result.outputs["e1.value"].iloc[0] == 12.0


def test_non_simulatable_plugin_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_entry_points(
        monkeypatch,
        [("bad", "tests.simulation.test_plugins:bad_factory")],
    )

    with pytest.raises(SimulationError, match="did not return a Simulatable"):
        create_element_from_plugin("bad")


def test_duplicate_plugin_names_raise(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_entry_points(
        monkeypatch,
        [("dup", "a:b"), ("dup", "c:d")],
    )

    with pytest.raises(SimulationError, match="Duplicate shrine.elements"):
        list_element_plugins()
