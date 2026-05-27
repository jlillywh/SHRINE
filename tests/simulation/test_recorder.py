"""Tests for shrine.simulation.recorder."""

from __future__ import annotations

import pandas as pd

from shrine.simulation import Clock, Recorder


class TestRecorder:
    def test_empty_dataframe(self) -> None:
        recorder = Recorder(Clock())
        assert recorder.to_dataframe().empty

    def test_records_multiple_variables_per_step(self) -> None:
        clock = Clock("1/1/2019", "1/3/2019")
        recorder = Recorder(clock)
        recorder.begin_timestep(clock.current_date)
        recorder.record("a", 1.0)
        recorder.record("b", 2.0)
        clock.advance()
        recorder.begin_timestep(clock.current_date)
        recorder.record("a", 3.0)
        recorder.record("b", 4.0)

        df = recorder.to_dataframe()
        assert list(df.columns) == ["a", "b"]
        assert len(df) == 2
        assert df["a"].iloc[0] == 1.0
        assert df["b"].iloc[1] == 4.0

    def test_reset_clears_rows(self) -> None:
        clock = Clock("1/1/2019", "1/2/2019")
        recorder = Recorder(clock)
        recorder.begin_timestep(clock.current_date)
        recorder.record("x", 1.0)
        recorder.reset()
        assert recorder.to_dataframe().empty

    def test_register_stores_unit_metadata(self) -> None:
        recorder = Recorder(Clock())
        recorder.register("flow", unit="m3/s")
        assert recorder.units["flow"] == "m3/s"

    def test_index_is_time(self) -> None:
        clock = Clock("1/1/2019", "1/2/2019")
        recorder = Recorder(clock)
        recorder.begin_timestep(clock.current_date)
        recorder.record("v", 1.0)
        df = recorder.to_dataframe()
        assert df.index.name == "time"
        assert isinstance(df.index[0], pd.Timestamp)

    def test_load_dataframe(self) -> None:
        index = pd.date_range("1/1/2019", periods=3)
        source = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [4.0, 5.0, 6.0]}, index=index)
        recorder = Recorder(Clock("1/1/2019", "1/3/2019"))
        recorder.load_dataframe(source)
        expected = source.copy()
        expected.index.name = "time"
        pd.testing.assert_frame_equal(recorder.to_dataframe(), expected, check_freq=False)

    def test_from_dataframe_classmethod(self) -> None:
        index = pd.date_range("1/1/2019", periods=2)
        source = pd.DataFrame({"flow": [10.0, 11.0]}, index=index)
        recorder = Recorder.from_dataframe(source)
        expected = source.copy()
        expected.index.name = "time"
        pd.testing.assert_frame_equal(recorder.to_dataframe(), expected, check_freq=False)
