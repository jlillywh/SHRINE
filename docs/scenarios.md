# Scenario configuration

Scenarios describe **run settings** separate from the physical model (elements and topology), which stay in Python code for now.

## File format

Supported extensions: `.json`, `.yaml`, `.yml`

Unknown keys at the top level, under `clock`, or inside typed `inputs` entries are **rejected at load time** with `SimulationError` (`phase=validate`). Optional `unit` strings are validated with **pint** when installed; otherwise a syntax check is used and a warning is emitted (install with `pip install -e .` for full validation).

### Allowed keys

| Section | Allowed keys |
|---------|----------------|
| Root | `name`, `seed`, `clock`, `inputs`, `overrides`, `metadata` |
| `clock` | `start_date`, `end_date`, `time_step`, `duration` |
| `inputs` (constant) | `type`, `value`, `unit` |
| `inputs` (monthly) | `type`, `values`, `unit` — month names must be English full names (`January`, …) |
| `inputs` (stochastic) | `type`, `distribution`, `loc`, `scale`, `low`, `high`, `unit` |
| `overrides` | Per-element mappings (validated when applied to the model) |
| `metadata` | Free-form user metadata |

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
    unit: mm/day                 # optional; validated with pint at load time
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
from shrine.simulation import load_scenario_file, run_scenario, run_scenarios

scenario = load_scenario_file("scenarios/baseline_watershed.json")
result = run_scenario(model, scenario)

results = run_scenarios(build_model, [scenario_a, scenario_b])
```

CLI example:

```bash
python examples/run_from_scenario.py scenarios/baseline_watershed.json
```

## Run metadata (SCN-03)

Each `RunResult` includes:

- **`result.manifest`** — structured provenance dict (preferred)
- **`result.metadata`** — superset (includes `manifest` nested for backward compatibility)

Manifest fields:

| Field | Description |
|-------|-------------|
| `run_id` | Unique id per run |
| `git_commit` | `git rev-parse HEAD` when run inside a git repo, else `null` |
| `scenario_name` | Scenario label |
| `scenario_hash` | SHA-256 of canonical scenario config (clock, inputs, overrides, seed) |
| `scenario_source_file` | Path from `load_scenario_file`, if any |
| `seed`, `reproducible` | Random seed policy (INP-04) |
| `started_at_utc`, `finished_at_utc` | Wall-clock ISO timestamps |
| `elapsed_seconds`, `status` | Run outcome |
| `elements` | `[{element_id, element_type, kind?}, …]` registered on the model |
| `framework_version`, `python_version` | Environment |

Legacy flat metadata keys (`run_id`, `scenario_name`, `seed`, …) remain on `result.metadata` as well.

## Reproducible seeds (INP-04, NFR-02)

Set `seed` on `RunController` or in a scenario file. Stochastic inputs draw from the run’s NumPy generator:

```python
from shrine.simulation import RunController, StochasticInput, InputManager

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
