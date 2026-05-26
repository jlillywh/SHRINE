"""Tests for scenario YAML/JSON configuration (SCN-*)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aegis.simulation import (
    Clock,
    Model,
    ScenarioConfig,
    WatershedElement,
    load_scenario_file,
    run_scenario,
    run_scenarios,
)
from aegis.simulation.errors import SimulationError, SimulationPhase
from hydrology.catchment import Catchment
from hydrology.watershed import Watershed
from tests.conftest import SimpleStore
from aegis.simulation.adapters import ReservoirElement


def _watershed_model() -> Model:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    model = Model(name="ScenarioTest", clock=Clock("1/1/2019", "1/10/2019"))
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


class TestScenarioConfig:
    def test_from_dict_constant_inputs(self) -> None:
        sc = ScenarioConfig.from_dict(
            {
                "name": "test",
                "inputs": {"precipitation": 8.0, "evaporation": 0.5},
            }
        )
        mgr = sc.build_input_manager()
        from aegis.simulation.context import RunContext, TimestepContext

        clock = Clock()
        run = RunContext(model_id="t", clock=clock)
        ctx = TimestepContext(
            run=run, step_index=0, current_time=clock.current_date, dt=clock.time_step
        )
        values = mgr.values_for_timestep(ctx)
        assert values["precipitation"] == 8.0

    def test_load_json_file(self, tmp_path: Path) -> None:
        path = tmp_path / "s.json"
        path.write_text(
            json.dumps(
                {
                    "name": "json_run",
                    "clock": {"start_date": "1/1/2019", "end_date": "1/4/2019"},
                    "inputs": {"precipitation": 10.0, "evaporation": 1.0},
                }
            ),
            encoding="utf-8",
        )
        sc = load_scenario_file(path)
        assert sc.name == "json_run"
        assert sc.metadata["source_file"] == str(path)

    def test_missing_name_raises(self) -> None:
        with pytest.raises(SimulationError) as exc_info:
            ScenarioConfig.from_dict({"inputs": {}})
        assert exc_info.value.phase == SimulationPhase.VALIDATE


class TestRunScenario:
    def test_run_scenario_applies_clock_and_inputs(self) -> None:
        sc = ScenarioConfig(
            name="dry",
            seed=99,
            clock={"start_date": "1/1/2019", "end_date": "1/5/2019"},
            inputs={"precipitation": 10.0, "evaporation": 1.0},
        )
        model = _watershed_model()
        result = run_scenario(model, sc, raise_on_error=False)
        assert result.success
        expected = Catchment().outflow(10.0, 1.0)
        assert result.outputs["basin.outflow"].iloc[0] == pytest.approx(expected, rel=1e-5)
        assert result.metadata["scenario_name"] == "dry"
        assert result.metadata["seed"] == 99
        assert result.metadata["framework_version"] == "0.1.0"
        assert "run_timestamp_utc" in result.metadata

    def test_run_scenarios_isolated(self) -> None:
        scenarios = [
            ScenarioConfig(
                name="a",
                clock={"start_date": "1/1/2019", "end_date": "1/3/2019"},
                inputs={"precipitation": 10.0, "evaporation": 1.0},
            ),
            ScenarioConfig(
                name="b",
                clock={"start_date": "1/1/2019", "end_date": "1/3/2019"},
                inputs={"precipitation": 5.0, "evaporation": 0.5},
            ),
        ]
        results = run_scenarios(_watershed_model, scenarios, raise_on_error=False)
        assert len(results) == 2
        assert results[0].metadata["scenario_name"] == "a"
        assert results[1].metadata["scenario_name"] == "b"
        assert results[0].outputs["basin.outflow"].iloc[0] != results[1].outputs["basin.outflow"].iloc[0]

    def test_element_override_release(self) -> None:
        store = SimpleStore(50.0)
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("res1", ReservoirElement(store, element_id="res1", release_key="release"))
        sc = ScenarioConfig(
            name="release_test",
            inputs={"inflow": 10.0},
            overrides={"res1": {"default_release": 8.0}},
        )
        result = run_scenario(model, sc, raise_on_error=False)
        assert result.success
        assert store.request == pytest.approx(8.0)


class TestBundledScenarios:
    def test_baseline_json_scenario_file(self) -> None:
        root = Path(__file__).resolve().parents[2]
        path = root / "scenarios" / "baseline_watershed.json"
        sc = load_scenario_file(path)
        result = run_scenario(_watershed_model(), sc, raise_on_error=False)
        assert result.success

    @pytest.mark.skipif(
        __import__("importlib").util.find_spec("yaml") is None,
        reason="PyYAML not installed",
    )
    def test_wet_year_yaml_scenario_file(self) -> None:
        root = Path(__file__).resolve().parents[2]
        path = root / "scenarios" / "wet_year.yaml"
        sc = load_scenario_file(path)
        assert sc.name == "wet_year"
        result = run_scenario(_watershed_model(), sc, raise_on_error=False)
        assert result.success
