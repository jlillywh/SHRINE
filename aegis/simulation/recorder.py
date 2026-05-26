"""Output recording (OUT-*)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from aegis.simulation.clock import Clock


class Recorder:
    """Records named outputs per timestep into a wide DataFrame."""

    def __init__(self, clock: Clock) -> None:
        self._clock = clock
        self._rows: list[dict[str, Any]] = []
        self._units: dict[str, str] = {}

    def register(self, variable: str, *, unit: str | None = None) -> None:
        if unit is not None:
            self._units[variable] = unit

    def begin_timestep(self, timestamp: pd.Timestamp) -> None:
        """Start a new output row for the current timestep."""
        self._rows.append({"time": timestamp})

    def record(
        self,
        variable: str,
        value: Any,
        *,
        unit: str | None = None,
    ) -> None:
        if unit is not None:
            self._units[variable] = unit
        if not self._rows:
            self.begin_timestep(self._clock.current_date)
        self._rows[-1][variable] = value

    def to_dataframe(self) -> pd.DataFrame:
        if not self._rows:
            return pd.DataFrame()
        df = pd.DataFrame(self._rows).set_index("time")
        df.index.name = "time"
        return df

    @property
    def units(self) -> dict[str, str]:
        return dict(self._units)

    def reset(self) -> None:
        self._rows.clear()

    def load_dataframe(self, df: pd.DataFrame) -> None:
        """Replace recorded rows from a wide time-indexed DataFrame."""
        self.reset()
        if df.empty:
            return
        frame = df.copy()
        if frame.index.name != "time":
            frame = frame.reset_index()
            if "time" not in frame.columns:
                frame = frame.rename(columns={frame.columns[0]: "time"})
            frame = frame.set_index("time")
        for ts, row in frame.iterrows():
            self.begin_timestep(pd.Timestamp(ts))
            for col, val in row.items():
                if pd.notna(val):
                    self.record(str(col), val)

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        clock: Clock | None = None,
    ) -> Recorder:
        """Build a recorder pre-filled from a wide DataFrame (time index)."""
        if clock is None:
            if df.empty:
                clock = Clock()
            else:
                index = pd.DatetimeIndex(df.index)
                step = index[1] - index[0] if len(index) > 1 else pd.Timedelta("1 days")
                clock = Clock(index[0], index[-1], time_step=step)
        recorder = cls(clock)
        recorder.load_dataframe(df)
        return recorder
