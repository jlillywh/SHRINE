# Scenario configuration

Scenarios describe **run settings** separate from the physical model (elements and topology), which stay in Python code for now.

## File format

Supported extensions: `.json`, `.yaml`, `.yml`

```yaml
name: my_scenario
seed: 42

clock:
  start_date: "1/1/2019"
  end_date: "1/31/2019"
  time_step: "1 days"
  # or: duration: "30 days"  (with start_date)

inputs:
  precipitation: 10.0          # shorthand constant
  evaporation:
    type: constant
    value: 1.0
  inflow:
    type: monthly
    values:
      January: 0.12
      February: 0.10
      # ... all month names for monthly inputs

overrides:
  res1:
    default_release: 5.0        # element attribute overrides (SCN-01)

metadata:
  description: Optional notes stored in run metadata
```

Bundled examples: `scenarios/baseline_watershed.json`, `scenarios/wet_year.yaml`.

## Python API

```python
from aegis.simulation import load_scenario_file, run_scenario, run_scenarios

scenario = load_scenario_file("scenarios/baseline_watershed.json")
result = run_scenario(model, scenario)

results = run_scenarios(build_model, [scenario_a, scenario_b])
```

CLI example:

```bash
python examples/run_from_scenario.py scenarios/baseline_watershed.json
```

## Run metadata (SCN-03)

Each `RunResult.metadata` includes:

- `run_id` — unique per run (differs on rerun even with the same seed)
- `scenario_name`, `seed`, `reproducible`, `start`, `end`, `time_step`, `num_timesteps`
- `model_name`, `status` (`success` / `failed`), `elapsed_seconds`
- `framework_version`, `run_timestamp_utc`, `python_version`
- `scenario_metadata` (from file, if present)

## Reproducible seeds (INP-04, NFR-02)

Set `seed` on `RunController` or in a scenario file. Stochastic inputs draw from the run’s NumPy generator:

```python
from aegis.simulation import RunController, StochasticInput, InputManager

inputs = InputManager()
inputs.bind("noise", StochasticInput("normal", loc=10.0, scale=0.5))
RunController(model, input_manager=inputs, seed=42).run()
```

Scenario YAML:

```yaml
seed: 42
inputs:
  noise:
    type: stochastic
    distribution: uniform
    low: 0.0
    high: 1.0
```

Same model + inputs + seed ⇒ identical outputs (within floating-point tolerance). Without a seed, deterministic elements still match; stochastic inputs are not reproducible across runs.
