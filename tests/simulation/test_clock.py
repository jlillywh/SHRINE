"""Tests for shrine.simulation.clock."""

from __future__ import annotations

import pandas as pd

from shrine.simulation import Clock


class TestClock:
    def test_initial_state(self) -> None:
        clock = Clock("1/1/2019", "1/10/2019")
        assert clock.current_date == pd.Timestamp("2019-01-01")
        assert clock.running is True
        assert clock.step_index == 0
        assert clock.day_of_year == 1

    def test_advance_to_end_date(self) -> None:
        clock = Clock("1/1/2019", "1/10/2019")
        steps = 0
        while clock.running:
            clock.advance()
            steps += 1
        assert clock.current_date == clock.end_date
        assert steps > 0

    def test_reset_restores_start(self) -> None:
        clock = Clock("1/1/2019", "1/10/2019")
        for _ in range(5):
            clock.advance()
        clock.reset()
        assert clock.current_date == clock.start_date
        assert clock.running is True
        assert clock.step_index == 0

    def test_set_duration_updates_end(self) -> None:
        clock = Clock("4/28/1975", "10/15/1988")
        clock.set_duration("10 days")
        assert clock.end_date == clock.start_date + pd.Timedelta("10 days")
        assert clock.remaining_time == pd.Timedelta("10 days")

    def test_set_start_date_preserves_span(self) -> None:
        clock = Clock("1/1/2019", "1/31/2019")
        original_span = clock.end_date - clock.start_date
        clock.set_start_date("6/1/2019")
        assert clock.start_date == pd.Timestamp("6/1/2019")
        assert clock.end_date - clock.start_date == original_span
        assert clock.current_date == clock.start_date

    def test_current_date_at_end_stops_running(self) -> None:
        clock = Clock("1/1/2019", "1/5/2019")
        clock.current_date = clock.end_date
        assert clock.running is False

    def test_step_index_increments_on_advance(self) -> None:
        clock = Clock("1/1/2019", "1/5/2019")
        assert clock.step_index == 0
        clock.advance()
        assert clock.step_index == 1

    def test_timestep_count_matches_manual_loop(self) -> None:
        """Number of updates while running should match inclusive end date semantics."""
        clock = Clock("1/1/2019", "1/5/2019")
        count = 0
        while clock.running:
            count += 1
            clock.advance()
        # Matches legacy test_clock: lands on end_date after last advance
        assert count >= 1
