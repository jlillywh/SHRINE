"""Tests for CSV time-series import (roadmap 3.14)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from hydrology.watershed import Watershed
from shrine.simulation import (
    Clock,
    InputManager,
    Model,
    ScenarioConfig,
    TimeSeriesCsvInput,
    WatershedElement,
    bind_csv_columns,
    load_csv_timeseries,
    load_scenario_file,
    run_scenario,
)
from shrine.simulation.context import RunContext, TimestepContext
from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.import_csv import (
    providers_from_csv_mapping,
    read_csv_timeseries,
    resolve_csv_path,
)


@pytest.fixture
def climate_csv(tmp_path: Path) -> Path:
    path = tmp_path / "climate.csv"
    path.write_text(
        "time,precipitation,evaporation\n"
        "2019-01-01,8.0,1.0\n"
        "2019-01-02,6.0,0.5\n"
        "2019-01-03,10.0,1.0\n",
        encoding="utf-8",
    )
    return path


def _watershed_model() -> Model:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    model = Model(name="CsvBasin", clock=Clock("1/1/2019", "1/5/2019"))
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


class TestImportCsv:
    def test_load_csv_timeseries(self, climate_csv: Path) -> None:
        provider = load_csv_timeseries(climate_csv, value_column="precipitation")
        assert isinstance(provider, TimeSeriesCsvInput)
        ctx = TimestepContext(
            run=RunContext(model_id="t", clock=Clock("1/1/2019", "1/3/2019")),
            step_index=0,
            current_time=pd.Timestamp("2019-01-02"),
            dt=pd.Timedelta("1 days"),
        )
        assert provider.value_at(ctx) == pytest.approx(6.0)

    def test_bind_csv_columns(self, climate_csv: Path) -> None:
        manager = InputManager()
        bind_csv_columns(
            manager,
            climate_csv,
            {"precipitation": "precipitation", "evaporation": "evaporation"},
        )
        ctx = TimestepContext(
            run=RunContext(model_id="t", clock=Clock("1/1/2019", "1/2/2019")),
            step_index=0,
            current_time=pd.Timestamp("2019-01-01"),
            dt=pd.Timedelta("1 days"),
        )
        values = manager.values_for_timestep(ctx)
        assert values["precipitation"] == pytest.approx(8.0)
        assert values["evaporation"] == pytest.approx(1.0)

    def test_providers_from_csv_mapping(self, climate_csv: Path) -> None:
        providers = providers_from_csv_mapping(
            climate_csv,
            {"precipitation": "precipitation"},
        )
        assert "precipitation" in providers

    def test_missing_csv_raises(self, tmp_path: Path) -> None:
        with pytest.raises(SimulationError) as exc_info:
            load_csv_timeseries(tmp_path / "missing.csv", value_column="x")
        assert exc_info.value.phase == SimulationPhase.VALIDATE

    def test_missing_column_raises(self, climate_csv: Path) -> None:
        with pytest.raises(SimulationError, match="missing value column"):
            load_csv_timeseries(climate_csv, value_column="not_a_column")

    def test_missing_timestep_raises(self, climate_csv: Path) -> None:
        provider = load_csv_timeseries(climate_csv, value_column="precipitation")
        ctx = TimestepContext(
            run=RunContext(model_id="t", clock=Clock("1/1/2019", "1/10/2019")),
            step_index=9,
            current_time=pd.Timestamp("2019-01-10"),
            dt=pd.Timedelta("1 days"),
        )
        with pytest.raises(SimulationError) as exc_info:
            provider.value_at(ctx)
        assert exc_info.value.phase == SimulationPhase.INPUT

    def test_resolve_csv_path_relative_to_base_dir(self, climate_csv: Path) -> None:
        base = climate_csv.parent
        resolved = resolve_csv_path(climate_csv.name, base_dir=base)
        assert resolved == climate_csv.resolve()

    def test_empty_csv_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "empty.csv"
        path.write_text("time,precipitation\n", encoding="utf-8")
        with pytest.raises(SimulationError, match="empty"):
            load_csv_timeseries(path, value_column="precipitation")

    def test_missing_time_column_raises(self, climate_csv: Path) -> None:
        with pytest.raises(SimulationError, match="missing time column"):
            load_csv_timeseries(climate_csv, time_column="not_time", value_column="precipitation")

    def test_providers_missing_mapped_column(self, climate_csv: Path) -> None:
        with pytest.raises(SimulationError, match="missing mapped column"):
            providers_from_csv_mapping(climate_csv, {"precipitation": "missing_col"})

    def test_time_series_csv_input_empty_series_raises(self) -> None:
        with pytest.raises(SimulationError, match="must not be empty"):
            TimeSeriesCsvInput(pd.Series(dtype=float))

    def test_exact_timestamp_lookup(self, climate_csv: Path) -> None:
        provider = load_csv_timeseries(climate_csv, value_column="precipitation")
        ctx = TimestepContext(
            run=RunContext(model_id="t", clock=Clock("1/1/2019", "1/3/2019")),
            step_index=0,
            current_time=pd.Timestamp("2019-01-01 00:00:00"),
            dt=pd.Timedelta("1 days"),
        )
        assert provider.value_at(ctx) == pytest.approx(8.0)


class TestCsvScenario:
    def test_bundled_csv_watershed_scenario(self) -> None:
        root = Path(__file__).resolve().parents[2]
        scenario = load_scenario_file(root / "scenarios" / "csv_watershed.yaml")
        result = run_scenario(_watershed_model(), scenario, raise_on_error=False)
        assert result.success
        assert len(result.outputs) == 14

    def test_scenario_csv_input_spec(self, tmp_path: Path, climate_csv: Path) -> None:
        scenario_path = tmp_path / "s.yaml"
        scenario_path.write_text(
            f"""
name: csv_test
clock:
  start_date: "1/1/2019"
  end_date: "1/3/2019"
inputs:
  precipitation:
    type: csv
    file: {climate_csv.name}
    column: precipitation
""".strip(),
            encoding="utf-8",
        )
        scenario = load_scenario_file(scenario_path)
        manager = scenario.build_input_manager()
        ctx = TimestepContext(
            run=RunContext(model_id="t", clock=Clock("1/1/2019", "1/3/2019")),
            step_index=2,
            current_time=pd.Timestamp("2019-01-03"),
            dt=pd.Timedelta("1 days"),
        )
        assert manager.values_for_timestep(ctx)["precipitation"] == pytest.approx(10.0)

    def test_scenario_csv_requires_column(self) -> None:
        with pytest.raises(SimulationError, match="requires 'column'"):
            ScenarioConfig.from_dict(
                {
                    "name": "bad",
                    "inputs": {"precipitation": {"type": "csv", "file": "x.csv"}},
                }
            )

    def test_scenario_value_column_alias(self, tmp_path: Path, climate_csv: Path) -> None:
        scenario_path = tmp_path / "s.yaml"
        scenario_path.write_text(
            f"""
name: csv_test
clock:
  start_date: "1/1/2019"
  end_date: "1/2/2019"
inputs:
  evaporation:
    type: csv
    file: {climate_csv.name}
    value_column: evaporation
""".strip(),
            encoding="utf-8",
        )
        scenario = load_scenario_file(scenario_path)
        manager = scenario.build_input_manager()
        ctx = TimestepContext(
            run=RunContext(model_id="t", clock=Clock("1/1/2019", "1/2/2019")),
            step_index=0,
            current_time=pd.Timestamp("2019-01-01"),
            dt=pd.Timedelta("1 days"),
        )
        assert manager.values_for_timestep(ctx)["evaporation"] == pytest.approx(1.0)

    def test_read_csv_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(SimulationError, match="not found"):
            read_csv_timeseries(tmp_path / "nope.csv")
