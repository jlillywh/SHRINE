"""Tests for shrine.simulation.recorder."""

from __future__ import annotations

import pandas as pd

import pytest

from shrine.simulation import Clock, Recorder
from shrine.simulation.errors import SimulationError, SimulationPhase


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

    def test_register_rejects_invalid_unit(self) -> None:
        recorder = Recorder(Clock())
        with pytest.raises(SimulationError) as exc_info:
            recorder.register("flow", unit="not_a_real_unit_xyz")
        assert exc_info.value.phase == SimulationPhase.RECORD

    def test_register_accepts_hydrology_rate(self) -> None:
        recorder = Recorder(Clock())
        recorder.register("precipitation", unit="mm/day")
        assert recorder.units["precipitation"] == "mm/day"

    def test_conflicting_units_raise(self) -> None:
        recorder = Recorder(Clock())
        recorder.register("flow", unit="m3/s")
        with pytest.raises(SimulationError) as exc_info:
            recorder.record("flow", 1.0, unit="ft3/s")
        assert exc_info.value.phase == SimulationPhase.RECORD
        assert "Conflicting units" in exc_info.value.message

    def test_record_unit_matches_register(self) -> None:
        recorder = Recorder(Clock())
        recorder.register("flow", unit="m3/s")
        recorder.begin_timestep(pd.Timestamp("2019-01-01"))
        recorder.record("flow", 10.0, unit="m3/s")
        assert recorder.units["flow"] == "m3/s"

    def test_equivalent_unit_aliases_keep_first_label(self) -> None:
        recorder = Recorder(Clock())
        recorder.register("flow", unit="m3/s")
        recorder.record("flow", 1.0, unit="m**3/s")
        assert recorder.units["flow"] == "m3/s"

    def test_strict_units_rejects_bare_float_without_metadata(self) -> None:
        recorder = Recorder(Clock(), strict_units=True)
        with pytest.raises(SimulationError) as exc_info:
            recorder.record("flow", 1.0)
        assert exc_info.value.phase == SimulationPhase.RECORD
        assert "strict_units" in exc_info.value.message

    def test_strict_units_allows_registered_unit_with_bare_float(self) -> None:
        recorder = Recorder(Clock(), strict_units=True)
        recorder.register("flow", unit="m3/s")
        recorder.begin_timestep(pd.Timestamp("2019-01-01"))
        recorder.record("flow", 10.0)
        assert recorder.units["flow"] == "m3/s"

    def test_strict_units_register_requires_unit(self) -> None:
        recorder = Recorder(Clock(), strict_units=True)
        with pytest.raises(SimulationError):
            recorder.register("flow")

    def test_strict_units_accepts_pint_quantity(self) -> None:
        from shrine.units import get_unit_registry

        ureg = get_unit_registry()
        recorder = Recorder(Clock(), strict_units=True)
        recorder.begin_timestep(pd.Timestamp("2019-01-01"))
        recorder.record("flow", ureg.Quantity(5.0, "m**3/s"))
        assert "flow" in recorder.units
