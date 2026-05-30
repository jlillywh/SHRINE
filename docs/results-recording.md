# Results recording (`TimeHistory` + `Recorder`)

Simulation runs record outputs through `shrine.simulation.Recorder` (wide DataFrame, time index). Legacy `results.TimeHistory` is now a thin wrapper around the same storage (OUT-04).

## Framework recording

Elements register variables in `initialize` and write each timestep in `update`:

```python
def initialize(self, run_context):
    run_context.recorder.register("outflow", unit="m3/s")

def update(self, timestep_context):
    timestep_context.recorder.record("outflow", self.outflow)
```

Unit strings on `register(..., unit=...)` and `record(..., unit=...)` are validated with the shared pint registry (`shrine.units.validate_unit_string`). Invalid units raise `SimulationError` with `phase=record`. The same variable cannot be assigned two different units in one run.

After the run, `recorder.units` maps each output column name to its unit string (OUT-02). The same map is stored on `RunResult.manifest["output_units"]` when units were registered.

### Strict unit mode

Set `strict_units=True` on `RunController` or `Recorder` to fail fast when an output is recorded as a bare number (`float` / `int`) without unit metadata. Each variable must either:

- be `register(..., unit="...")` before the first `record`, or
- receive `unit=` on `record`, or
- be a pint `Quantity` (units taken from the value).

Default is `strict_units=False` so legacy adapters without unit metadata keep working.

`RunController` calls `recorder.begin_timestep()` before element updates.

## Export to CSV + JSON (roadmap **3.13**)

For Excel and report workflows, write tabular outputs and provenance to a folder:

```python
from pathlib import Path
from shrine.simulation import export_run_result, load_and_run

result = load_and_run(build_model, "scenarios/baseline_watershed.json")
csv_path, manifest_path = export_run_result(result, Path("my_run"))
```

Creates:

| File | Contents |
|------|----------|
| `results.csv` | Wide table with a `time` column (date strings) and one column per recorded variable |
| `run_manifest.json` | Run provenance (`scenario_name`, `scenario_hash`, `seed`, timestamps, `framework_version`, …) plus `output_units`, `outputs_columns`, `export_format_version` |

CLI example:

```bash
.venv/bin/python3 examples/export_run_results.py scenarios/baseline_watershed.json ./my_run
```

NetCDF and Parquet export are deferred (see [modernization roadmap](modernization-roadmap.md) **3.13+**).

## `TimeHistory` (legacy / plotting)

```python
from results.time_history import TimeHistory
from shrine.simulation import RunController

result = RunController(model, input_manager=inputs).run()
history = TimeHistory.from_run_result(result, name="Climate Results", display_unit="in")
history.show()  # optional matplotlib
```

Manual assembly (e.g. port of `test_model.py`):

```python
th = TimeHistory("Climate", "in", clock)
th.add_series(evaporation_series)
th.add_series(precipitation_series)
```

Factories: `from_recorder`, `from_dataframe`, `from_run_result`.

## `Recorder` utilities

- `Recorder.from_dataframe(df)` — build from existing results
- `recorder.load_dataframe(df)` — replace rows in place
