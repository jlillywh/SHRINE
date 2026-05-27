"""Time series results storage backed by :class:`~shrine.simulation.recorder.Recorder`."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

from shrine.simulation.clock import Clock as SimulationClock
from shrine.simulation.recorder import Recorder
from global_attributes.shrine_object import ShrineObject

if TYPE_CHECKING:
    from shrine.simulation.run_controller import RunResult


def _adapt_clock(clock: Any) -> SimulationClock:
    """Convert legacy ``global_attributes.clock.Clock`` to simulation clock."""
    if isinstance(clock, SimulationClock):
        return clock
    return SimulationClock(
        start_date=clock.start_date,
        end_date=clock.end_date,
        time_step=clock.time_step,
    )


class TimeHistory(ShrineObject):
    """Store and plot time series using the simulation :class:`Recorder` (OUT-04).

    Legacy code can still call :meth:`add_series` and :meth:`show`. Framework runs
    should record via ``RunContext.recorder`` or build from :meth:`from_dataframe`.
    """

    def __init__(
        self,
        name: str = "TimeHistory",
        display_unit: str = "in",
        clock: Any | None = None,
        *,
        recorder: Recorder | None = None,
    ) -> None:
        ShrineObject.__init__(self)
        self.name = name
        self.unit = display_unit
        self.th_list: list[pd.Series] = []
        if recorder is not None:
            self._recorder = recorder
        else:
            sim_clock = _adapt_clock(clock or SimulationClock())
            self._recorder = Recorder(sim_clock)

    @property
    def recorder(self) -> Recorder:
        return self._recorder

    @property
    def series(self) -> pd.DataFrame:
        """Wide DataFrame of recorded variables (time index)."""
        return self._recorder.to_dataframe()

    @series.setter
    def series(self, value: pd.Series | pd.DataFrame) -> None:
        if isinstance(value, pd.Series):
            frame = value.to_frame()
        elif isinstance(value, pd.DataFrame):
            frame = value
        else:
            raise TypeError("series must be a pandas Series or DataFrame")
        self._load_dataframe(frame)

    def set_value(self, series_name: str, at_date: str | pd.Timestamp, value: Any) -> None:
        """Set one value for a named column at a calendar timestamp."""
        ts = pd.Timestamp(at_date)
        df = self.series
        if df.empty or ts not in df.index:
            self._recorder.begin_timestep(ts)
            self._recorder.record(series_name, value, unit=self.unit)
            return
        updated = df.copy()
        if series_name not in updated.columns:
            updated[series_name] = pd.NA
        updated.loc[ts, series_name] = value
        self._load_dataframe(updated)

    def add_series(self, new_series: pd.Series) -> None:
        """Add a named series column (legacy API; prefer framework recording)."""
        if new_series.name is None:
            raise ValueError("Series must be named")
        self.th_list.append(new_series)
        self._recorder.register(str(new_series.name), unit=self.unit)
        df = self.series
        if df.empty:
            frame = new_series.to_frame()
        else:
            frame = df.join(new_series.rename(new_series.name), how="outer")
        self._load_dataframe(frame)

    def load_csv(self, file_path: str) -> None:
        """Load a wide CSV with a time index column."""
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        self._load_dataframe(df)

    @classmethod
    def from_recorder(
        cls,
        recorder: Recorder,
        *,
        name: str = "TimeHistory",
        display_unit: str = "in",
    ) -> TimeHistory:
        return cls(name=name, display_unit=display_unit, recorder=recorder)

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        *,
        name: str = "TimeHistory",
        display_unit: str = "in",
    ) -> TimeHistory:
        recorder = Recorder.from_dataframe(df)
        return cls(name=name, display_unit=display_unit, recorder=recorder)

    @classmethod
    def from_run_result(
        cls,
        result: RunResult,
        *,
        name: str = "TimeHistory",
        display_unit: str = "in",
    ) -> TimeHistory:
        return cls.from_dataframe(result.outputs, name=name, display_unit=display_unit)

    def _load_dataframe(self, df: pd.DataFrame) -> None:
        self._recorder.load_dataframe(df)

    def show(self) -> None:
        """Plot recorded series (requires matplotlib)."""
        import matplotlib.pyplot as plt

        if self.series.empty:
            return
        self.series.plot(title=self.name)
        plt.ylabel(self.unit)
        plt.tight_layout()
        plt.show()
