"""DEPRECATED: Colocated unittest — migrate to tests/inputs/ (roadmap 2.11)."""

from __future__ import annotations

from testing.colocated import deprecate_colocated_module

deprecate_colocated_module(path="inputs.test_timeseries", migrated_to="tests/inputs/ (pending)")

import datetime
from datetime import timedelta
from unittest import TestCase

from inputs.time_series import TimeSeries


class TestTimeSeries(TestCase):
    def setUp(self):
        """Set up a new object to be tested"""
        self.ts = TimeSeries("1/1/19", periods=365)
        self.dec_places = 3

    def tearDown(self):
        """Destroy the object after running tests"""
        del self.ts

    def test_num_of_records(self):
        nr = 365
        self.assertEqual(self.ts.num_of_records(), nr)

    def test_start_date(self):
        sd = datetime.date(2019, 1, 1)
        self.assertEqual(self.ts.start_date(), sd)

    def test_end_date(self):
        ed = datetime.date(2019, 12, 31)
        self.assertEqual(self.ts.end_date(), ed)

    def test_duration(self):
        dur = timedelta(days=365)
        self.assertEqual(self.ts.duration(), dur)
