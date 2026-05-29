"""Tests for shared unit registry and RunContext injection."""

from __future__ import annotations

from shrine.simulation import (
    Clock,
    Model,
    RunContext,
    RunController,
)
from shrine.units import (
    SHRINE_UNITS_JSON,
    get_default_units,
    get_unit_registry,
    load_units,
    reset_unit_caches,
    validate_unit_string,
)


class TestShrineUnits:
    def setup_method(self) -> None:
        reset_unit_caches()

    def teardown_method(self) -> None:
        reset_unit_caches()

    def test_default_units_loaded_once(self) -> None:
        assert SHRINE_UNITS_JSON.is_file()
        first = get_default_units()
        second = get_default_units()
        assert first is second
        assert first["length"] == "m"
        assert first["time"] == "day"

    def test_unit_registry_singleton(self) -> None:
        assert get_unit_registry() is get_unit_registry()

    def test_validate_hydrology_flow_unit(self) -> None:
        assert validate_unit_string("m3/s", field="test") == "m3/s"
        assert validate_unit_string("mm/day", field="test") == "mm/day"

    def test_run_context_injects_registry(self) -> None:
        clock = Clock("1/1/2019", "1/2/2019")
        run = RunContext(model_id="t", clock=clock)
        assert run.units_registry is get_unit_registry()
        assert run.default_units is get_default_units()
        assert run.default_units["mass"] == "kg"

    def test_load_units_custom_file(self, tmp_path) -> None:
        path = tmp_path / "units.json"
        path.write_text('{"length": "ft", "time": "hour"}', encoding="utf-8")
        loaded = load_units(path)
        assert loaded == {"length": "ft", "time": "hour"}


class TestRunControllerUnits:
    def test_initialize_receives_shared_registry(self) -> None:
        captured: list[RunContext] = []

        class _Probe:
            element_type = "probe"

            def initialize(self, run_context: RunContext) -> None:
                captured.append(run_context)

            def update(self, _timestep_context) -> None:
                pass

            def finalize(self, _run_context: RunContext) -> None:
                pass

        model = Model(clock=Clock("1/1/2019", "1/2/2019"))
        model.register("p", _Probe())
        RunController(model, raise_on_error=False).run()
        assert len(captured) == 1
        assert captured[0].units_registry is get_unit_registry()
        assert captured[0].default_units is get_default_units()
