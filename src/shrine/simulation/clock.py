"""Simulation clock (CLK-*)."""

from __future__ import annotations

import pandas as pd


class Clock:
    """Calendar clock for simulation time stepping.

    v1 uses a single uniform ``time_step`` for all elements (CLK-08).
    """

    def __init__(
        self,
        start_date: str | pd.Timestamp = "1/1/2019",
        end_date: str | pd.Timestamp = "1/1/2020",
        time_step: str | pd.Timedelta = "1 days",
    ) -> None:
        self.start_date = pd.Timestamp(start_date)
        self.end_date = pd.Timestamp(end_date)
        self.duration = self.end_date - self.start_date
        self.range = pd.date_range(start=self.start_date, end=self.end_date)
        self.time_step = pd.Timedelta(time_step)

        self._current_date = self.start_date
        self.remaining_time = self.duration
        self.running = True
        self.step_index = 0
        self.day_of_year = self._current_date.dayofyear

    @property
    def current_date(self) -> pd.Timestamp:
        return self._current_date

    @current_date.setter
    def current_date(self, new_date: str | pd.Timestamp) -> None:
        self._current_date = self._to_timestamp(new_date)
        if self._current_date >= self.end_date:
            self.running = False
            self.duration = pd.Timedelta("0 days")
        else:
            self.duration = self.end_date - self._current_date

        self.remaining_time = self.duration
        self.day_of_year = self._current_date.dayofyear

    def reset(self) -> None:
        """Reset to initial time for another run."""
        self._current_date = self.start_date
        self.remaining_time = self.end_date - self.start_date
        self.duration = self.remaining_time
        self.running = True
        self.step_index = 0
        self.day_of_year = self._current_date.dayofyear

    def advance(self) -> None:
        """Advance one timestep; stop when ``current_date`` reaches ``end_date``."""
        if self._current_date >= self.end_date:
            self.running = False
        else:
            self._current_date += self.time_step
            self.remaining_time -= self.time_step
            self.step_index += 1
            self.day_of_year = self._current_date.dayofyear

    def set_start_date(self, new_date: str | pd.Timestamp) -> None:
        """Change start date while keeping duration; reset current time."""
        span = self.end_date - self.start_date
        self.start_date = self._to_timestamp(new_date)
        self._current_date = self.start_date
        self.end_date = self.start_date + span
        self.duration = span
        self.remaining_time = self.duration
        self.running = True
        self.range = pd.date_range(start=self.start_date, end=self.end_date)
        self.step_index = 0
        self.day_of_year = self._current_date.dayofyear

    def set_duration(self, new_duration: str | pd.Timedelta) -> None:
        """Change run duration and recompute ``end_date`` from ``start_date``."""
        self.duration = pd.Timedelta(new_duration)
        self.remaining_time = self.duration
        self.end_date = self.start_date + self.duration
        self.range = pd.date_range(start=self.start_date, end=self.end_date)

    @staticmethod
    def _to_timestamp(value: str | pd.Timestamp) -> pd.Timestamp:
        """Parse a calendar timestamp (pandas 2.x: no ``freq`` on Timestamp)."""
        return pd.Timestamp(value)
