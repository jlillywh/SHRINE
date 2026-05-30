"""Tests for CSV + JSON run export (roadmap 3.13)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from hydrology.watershed import Watershed
from shrine.simulation import (
    Clock,
    Model,
    ScenarioConfig,
    WatershedElement,
    export_run_result,
    run_scenario,
)
from shrine.simulation.export import build_export_manifest, outputs_to_csv_frame
from shrine.simulation.run_controller import RunResult


def _watershed_model() -> Model:
    ws = Watershed()
    ws.add_junction("J1", "sink")
    ws.link_catchment("C1", "J1")
    model = Model(name="ExportBasin", clock=Clock("1/1/2019", "1/5/2019"))
    model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
    return model


class TestExportRunResult:
    def test_outputs_to_csv_frame_adds_time_column(self) -> None:
        index = pd.date_range("2019-01-01", periods=3, freq="D")
        outputs = pd.DataFrame({"basin.outflow": [1.0, 2.0, 3.0]}, index=index)
        outputs.index.name = "time"
        frame = outputs_to_csv_frame(outputs)
        assert list(frame.columns) == ["time", "basin.outflow"]
        assert frame["time"].tolist() == ["2019-01-01", "2019-01-02", "2019-01-03"]

    def test_export_writes_csv_and_manifest(self, tmp_path: Path) -> None:
        scenario = ScenarioConfig(
            name="export_test",
            seed=42,
            clock={"start_date": "1/1/2019", "end_date": "1/5/2019"},
            inputs={"precipitation": 10.0, "evaporation": 1.0},
        )
        result = run_scenario(_watershed_model(), scenario, raise_on_error=False)
        assert result.success

        csv_path, manifest_path = export_run_result(result, tmp_path)
        assert csv_path == tmp_path / "results.csv"
        assert manifest_path == tmp_path / "run_manifest.json"
        assert csv_path.is_file()
        assert manifest_path.is_file()

        frame = pd.read_csv(csv_path)
        assert "time" in frame.columns
        assert "basin.outflow" in frame.columns
        assert len(frame) == 5

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["scenario_name"] == "export_test"
        assert manifest["seed"] == 42
        assert manifest["framework_version"]
        assert manifest["outputs_file"] == "results.csv"
        assert manifest["export_format_version"] == "1.0"
        assert manifest["outputs_row_count"] == 5
        assert "basin.outflow" in manifest["outputs_columns"]
        assert manifest["started_at_utc"]
        assert manifest["finished_at_utc"]

    def test_build_export_manifest_includes_units_when_present(self) -> None:
        result = RunResult(
            success=True,
            outputs=pd.DataFrame({"flow": [1.0]}),
            manifest={
                "scenario_name": "x",
                "output_units": {"flow": "m3/s"},
            },
        )
        manifest = build_export_manifest(result)
        assert manifest["output_units"] == {"flow": "m3/s"}

    def test_export_custom_filenames(self, tmp_path: Path) -> None:
        result = RunResult(
            success=True, outputs=pd.DataFrame(), manifest={"scenario_name": "empty"}
        )
        csv_path, manifest_path = export_run_result(
            result,
            tmp_path,
            csv_name="out.csv",
            manifest_name="meta.json",
        )
        assert csv_path.name == "out.csv"
        assert manifest_path.name == "meta.json"
