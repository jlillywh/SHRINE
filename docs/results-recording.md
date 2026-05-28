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

After the run, `recorder.units` maps each output column name to its unit string (OUT-02).

### Strict unit mode

Set `strict_units=True` on `RunController` or `Recorder` to fail fast when an output is recorded as a bare number (`float` / `int`) without unit metadata. Each variable must either:

- be `register(..., unit="...")` before the first `record`, or
- receive `unit=` on `record`, or
- be a pint `Quantity` (units taken from the value).

Default is `strict_units=False` so legacy adapters without unit metadata keep working.

`RunController` calls `recorder.begin_timestep()` before element updates.

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
