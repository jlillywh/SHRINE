"""DEPRECATED: Legacy manual model script — prefer examples/ and pytest tests/ (roadmap 2.11)."""

from __future__ import annotations

from testing.colocated import deprecate_colocated_module

deprecate_colocated_module(
    path="global_attributes.test_model", migrated_to="examples/ and tests/simulation/"
)

from data.fileman import FileManager
from tests.path_fixtures import REPO_ROOT
import pandas as pd
from inputs.data import Vector
from results.time_history import TimeHistory
from global_attributes.clock import Clock


"""Legacy script — manual clock loop. Prefer examples/climate_loop.py (shrine.simulation).

    Results: build TimeHistory via add_series, or TimeHistory.from_dataframe after a
    framework run (see docs/results-recording.md).

    This model replicates the work done in the IWRM SLC V9.111.gsm model."""
fm = FileManager(REPO_ROOT / "data_external")
input_file = fm.add_file("data.xlsx")

xls_file = pd.ExcelFile(input_file)

monthly_data = pd.read_excel(xls_file, "Monthly")
xls_file.close()

c = Clock()

evap_table = Vector("Evaporation", "in", monthly_data["Evap"])
precip_table = Vector("Precipitation", "in", monthly_data["Precip"])

e_ts = pd.Series(name="evaporation")
p_ts = pd.Series(name="precip")
th1 = TimeHistory("Climate Results", "in", c)


while c.running:
    """Set up the run properties"""
    month = c.current_date.month_name()
    dayofyear = c.current_date.dayofyear

    """Define input variables"""
    evap_rate = evap_table[month]
    precip_rate = precip_table[month]

    """Append daily results to time series"""
    e_ts[c.current_date] = evap_rate
    p_ts[c.current_date] = precip_rate

    """Advance the simulation clock forward by a time step"""
    c.advance()

th1.add_series(e_ts)
th1.add_series(p_ts)

th1.show()
