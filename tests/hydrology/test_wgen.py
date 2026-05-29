"""WGEN stochastic weather generator (migrated from src/hydrology/test_wgen.py)."""

from __future__ import annotations

import numpy as np
import pytest

from hydrology.wgen import Wgen


@pytest.fixture
def wgen() -> Wgen:
    return Wgen()


class TestWgen:
    def test_one_day_rain(self, wgen: Wgen) -> None:
        realizations = 100
        rain_total = 0.0
        for _ in range(realizations):
            wgen.update()
            rain_total += wgen.rain
        assert rain_total / realizations == pytest.approx(0.0488, abs=0.1)

    def test_monthly_rain(self, wgen: Wgen, legacy_clock) -> None:
        rain_obs = [
            1.41,
            1.68,
            2.51,
            3.63,
            4.45,
            4.15,
            3.95,
            2.84,
            4.00,
            3.12,
            1.58,
            1.66,
        ]
        rain_array = [0.0] * 12
        realizations = 200
        wgen.min_rain = 0.0
        for _ in range(1, realizations):
            legacy_clock.reset()
            while legacy_clock.running:
                month = legacy_clock.current_date.month - 1
                wgen.update(legacy_clock.current_date)
                rain_array[month] += wgen.rain
                legacy_clock.advance()

        for i in range(12):
            rain_array[i] /= realizations

        np.testing.assert_allclose(
            rain_obs,
            rain_array,
            rtol=0.15,
            atol=0.1,
            err_msg="Monthly rain not close enough",
        )

    def test_deterministic_temperature(self, wgen: Wgen, legacy_clock) -> None:
        goldsim_tavg = [
            19.19,
            19.04,
            23.47,
            33.7,
            47.97,
            63.43,
            73.54,
            74.41,
            65.17,
            50.55,
            35.4,
            24.74,
        ]
        wgen.temp_determ = True
        wgen.rain_deterministic = True
        wgen.markov_deterministic = True
        monthly_temps: list[float] = []
        while legacy_clock.running:
            wgen.update(legacy_clock.current_date)
            if legacy_clock.current_date.day == 1 and legacy_clock.current_date.year == 2019:
                monthly_temps.append(wgen.tavg)
            legacy_clock.advance()

        np.testing.assert_almost_equal(
            goldsim_tavg, monthly_temps, decimal=2, err_msg="Deterministic temps differ"
        )

    def test_average_temperature_by_month(self, wgen: Wgen, legacy_clock) -> None:
        observed_tavg = [
            28.99,
            33.75,
            41.5,
            55.37,
            65.06,
            73.66,
            78.14,
            76.57,
            68.98,
            58.03,
            44.17,
            33.45,
        ]
        realizations = 100
        monthly_temps = [0.0] * 12

        for _ in range(1, realizations):
            legacy_clock.reset()
            while legacy_clock.running:
                month = legacy_clock.current_date.month - 1
                wgen.update(legacy_clock.current_date)
                monthly_temps[month] += wgen.tavg / legacy_clock.current_date.daysinmonth
                legacy_clock.advance()

        for i in range(12):
            monthly_temps[i] /= realizations

        np.testing.assert_allclose(
            observed_tavg,
            monthly_temps,
            rtol=0.1,
            atol=0.05,
            err_msg="Avg temps not close enough",
        )
