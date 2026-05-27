"""Tests for results.TimeHistory backed by simulation Recorder."""

from __future__ import annotations

import pandas as pd

from shrine.simulation import Clock, Recorder, RunController
from examples.climate_loop import build_climate_model
from results.time_history import TimeHistory


class TestTimeHistoryRecorder:
    def test_empty_series_dataframe(self) -> None:
        th = TimeHistory(clock=Clock("1/1/2019", "1/3/2019"))
        assert th.series.empty
        assert isinstance(th.recorder, Recorder)

    def test_add_series_builds_dataframe(self) -> None:
        th = TimeHistory("Test", "in", Clock("1/1/2019", "1/4/2019"))
        evap = pd.Series([0.1, 0.2, 0.3], index=pd.date_range("1/1/2019", periods=3), name="evaporation")
        precip = pd.Series([0.5, 0.6, 0.7], index=pd.date_range("1/1/2019", periods=3), name="precipitation")
        th.add_series(evap)
        th.add_series(precip)
        assert list(th.series.columns) == ["evaporation", "precipitation"]
        assert th.series["evaporation"].iloc[0] == 0.1
        assert len(th.th_list) == 2

    def test_set_value_on_existing_column(self) -> None:
        th = TimeHistory(clock=Clock("1/1/2019", "1/3/2019"))
        th.set_value("flow", "1/1/2019", 10.0)
        th.set_value("flow", "1/2/2019", 12.0)
        assert th.series.loc[pd.Timestamp("1/2/2019"), "flow"] == 12.0

    def test_from_dataframe_round_trip(self) -> None:
        index = pd.date_range("1/1/2019", periods=3)
        df = pd.DataFrame({"a": [1.0, 2.0, 3.0]}, index=index)
        th = TimeHistory.from_dataframe(df, name="Imported")
        expected = df.copy()
        expected.index.name = "time"
        pd.testing.assert_frame_equal(th.series, expected, check_freq=False)

    def test_from_run_result_matches_recorder(self) -> None:
        _, controller = build_climate_model(start="1/1/2019", end="1/5/2019")
        result = controller.run()
        th = TimeHistory.from_run_result(result, name="Climate")
        pd.testing.assert_frame_equal(th.series, result.outputs)

    def test_recorder_from_dataframe(self) -> None:
        index = pd.date_range("1/1/2019", periods=2)
        df = pd.DataFrame({"x": [1.0, 2.0]}, index=index)
        recorder = Recorder.from_dataframe(df)
        expected = df.copy()
        expected.index.name = "time"
        pd.testing.assert_frame_equal(recorder.to_dataframe(), expected, check_freq=False)
