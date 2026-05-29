"""Tests for scenario YAML/JSON configuration (SCN-*)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from hydrology.catchment import Catchment
from hydrology.watershed import Watershed
from shrine.simulation import (
    Clock,
    Model,
    ScenarioConfig,
    WatershedElement,
    load_scenario_file,
    run_scenario,
    run_scenarios,
)
from shrine.simulation.adapters import ReservoirElement
from shrine.simulation.errors import SimulationError, SimulationPhase
from tests.conftest import SimpleStore


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
        from shrine.simulation.context import RunContext, TimestepContext

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

    def test_unknown_top_level_key_raises(self) -> None:
        with pytest.raises(SimulationError, match="Unknown keys in scenario"):
            ScenarioConfig.from_dict({"name": "x", "extra_field": 1})

    def test_unknown_clock_key_raises(self) -> None:
        with pytest.raises(SimulationError, match="Unknown keys in clock"):
            ScenarioConfig.from_dict(
                {
                    "name": "x",
                    "clock": {"start_date": "1/1/2019", "bad": True},
                }
            )

    def test_invalid_clock_time_step_raises(self) -> None:
        with pytest.raises(SimulationError, match="Invalid duration in clock.time_step"):
            ScenarioConfig.from_dict(
                {
                    "name": "x",
                    "clock": {"time_step": "not-a-duration"},
                }
            )

    def test_unknown_input_key_raises(self) -> None:
        with pytest.raises(SimulationError, match="Unknown keys in inputs.precipitation"):
            ScenarioConfig.from_dict(
                {
                    "name": "x",
                    "inputs": {
                        "precipitation": {
                            "type": "constant",
                            "value": 1.0,
                            "extra": True,
                        }
                    },
                }
            )

    def test_invalid_input_unit_raises(self) -> None:
        if not importlib.util.find_spec("pint"):
            pytest.skip("pint required for semantic unit validation")
        with pytest.raises(SimulationError, match="Invalid unit in inputs.evaporation.unit"):
            ScenarioConfig.from_dict(
                {
                    "name": "x",
                    "inputs": {
                        "evaporation": {
                            "type": "constant",
                            "value": 1.0,
                            "unit": "not_a_real_unit_xyz",
                        }
                    },
                }
            )

    def test_valid_input_unit_accepted(self) -> None:
        sc = ScenarioConfig.from_dict(
            {
                "name": "x",
                "inputs": {
                    "precipitation": {
                        "type": "constant",
                        "value": 1.0,
                        "unit": "mm/day",
                    }
                },
            }
        )
        assert sc.inputs["precipitation"]["unit"] == "mm/day"

    def test_unknown_month_in_monthly_input_raises(self) -> None:
        with pytest.raises(SimulationError, match="unknown month names"):
            ScenarioConfig.from_dict(
                {
                    "name": "x",
                    "inputs": {
                        "precipitation": {
                            "type": "monthly",
                            "values": {"NotAMonth": 1.0},
                        }
                    },
                }
            )


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
        assert result.manifest["scenario_hash"] is not None
        assert result.manifest["elements"]
        assert "git_commit" in result.manifest
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
        assert (
            results[0].outputs["basin.outflow"].iloc[0]
            != results[1].outputs["basin.outflow"].iloc[0]
        )

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

    def test_reservoir_override_unknown_key(self) -> None:
        store = SimpleStore(50.0)
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("res1", ReservoirElement(store, element_id="res1"))
        sc = ScenarioConfig(
            name="bad_override",
            overrides={"res1": {"not_a_field": 1.0}},
        )
        with pytest.raises(SimulationError) as exc_info:
            sc.apply_element_overrides(model)
        assert exc_info.value.phase == SimulationPhase.VALIDATE
        assert "not_a_field" in exc_info.value.message

    def test_reservoir_override_store_capacity(self) -> None:
        store = SimpleStore(50.0, capacity=200.0)
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("res1", ReservoirElement(store, element_id="res1"))
        sc = ScenarioConfig(name="cap", overrides={"res1": {"capacity": 80.0}})
        sc.apply_element_overrides(model)
        assert store.capacity == pytest.approx(80.0)


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
