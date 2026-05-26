"""Tests for aegis.simulation.recorder."""

from __future__ import annotations

import pandas as pd

from aegis.simulation import Clock, Recorder


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
