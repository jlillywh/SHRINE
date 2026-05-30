# Import time series from CSV (roadmap 3.14)

SHRINE can drive simulation inputs from **CSV files** — the format civil engineers already use in Excel. This pairs with [CSV export](results-recording.md#export-to-csv-json-roadmap-313) from **3.13**.

---

## CSV layout

| Column | Required | Description |
|--------|----------|-------------|
| `time` (default name) | Yes | Dates or timestamps (`2019-01-01` or `2019-01-01 08:00:00`) |
| Value columns | Yes | One or more numeric series (`precipitation`, `evaporation`, …) |

Example (`scenarios/data/jan2019_climate.csv`):

```csv
time,precipitation,evaporation
2019-01-01,8.0,1.0
2019-01-02,8.0,1.0
```

Daily runs use **date matching** (midnight-normalized) so Excel date strings work even when the clock stores full timestamps.

---

## Scenario YAML (`type: csv`)

Map each **simulation input name** to a **CSV column**. The `file` path is relative to the **scenario file** directory.

```yaml
name: csv_watershed
seed: 42

clock:
  start_date: "1/1/2019"
  end_date: "1/14/2019"
  time_step: "1 days"

inputs:
  precipitation:
    type: csv
    file: data/jan2019_climate.csv
    time_column: time          # optional; default "time"
    column: precipitation      # or value_column
  evaporation:
    type: csv
    file: data/jan2019_climate.csv
    column: evaporation

metadata:
  description: CSV-driven climate example
```

Bundled example: [`scenarios/csv_watershed.yaml`](https://github.com/jlillywh/SHRINE/blob/master/scenarios/csv_watershed.yaml).

Run:

```bash
.venv/bin/python3 examples/run_from_csv_scenario.py
```

---

## Python API

### One column

```python
from shrine.simulation import InputManager, load_csv_timeseries

manager = InputManager()
manager.bind("precipitation", load_csv_timeseries(
    "data/jan2019_climate.csv",
    value_column="precipitation",
))
```

### Column mapping (one file → many inputs)

```python
from shrine.simulation import InputManager, bind_csv_columns

manager = InputManager()
bind_csv_columns(
    manager,
    "scenarios/data/jan2019_climate.csv",
    {"precipitation": "precipitation", "evaporation": "evaporation"},
)
```

Or build providers without a manager:

```python
from shrine.simulation.import_csv import providers_from_csv_mapping

providers = providers_from_csv_mapping(
    "scenarios/data/jan2019_climate.csv",
    {"precipitation": "precipitation", "evaporation": "evaporation"},
)
```

Use `TimeSeriesCsvInput` via `load_csv_timeseries` or scenario `type: csv`; it implements the same `InputProvider` protocol as `ConstantInput` and `MonthlyLookupInput`.

---

## Column mapping reference

| Scenario key | Maps to |
|--------------|---------|
| `inputs.precipitation` | Model global input `precipitation` at each timestep |
| `column: precipitation` | Header cell in the CSV |
| `file` | Path to `.csv` (relative to scenario file or absolute) |
| `time_column` | Header for the date/time column (default `time`) |

Watershed adapters read `precipitation` and `evaporation` from the input manager each timestep — names must match what your elements expect.

---

## Errors

| Situation | Result |
|-----------|--------|
| Missing CSV file | `SimulationError`, `phase=validate` |
| Unknown column name | `SimulationError`, `phase=validate` |
| Timestep with no CSV row | `SimulationError`, `phase=input` |

---

## Related

- [Scenarios](scenarios.md) — other input types (`constant`, `monthly`, `stochastic`)
- [Results recording — export](results-recording.md#export-to-csv-json-roadmap-313) — write `results.csv` + manifest after a run
