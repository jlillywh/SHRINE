# Quickstart

This guide runs a two-catchment watershed model from a bundled scenario file. It uses the **supported** `shrine.simulation` path only.

## Prerequisites

Complete [Install](install.md):

```bash
pip install -e ".[dev]"
```

## 1. Build a model in Python

Topology and elements are defined in code. Scenario files supply clock, inputs, and parameter overrides.

```python
from hydrology.watershed import Watershed
from shrine.simulation import Model, WatershedElement

ws = Watershed()
ws.add_junction("J1", "sink")
ws.link_catchment("C1", "J1")
ws.link_catchment("C2", "J1")

model = Model(name="Basin")
model.register_watershed("basin", WatershedElement(ws, element_id="basin"))
```

## 2. Run from a scenario file

Bundled scenarios live in `scenarios/` at the repo root.

```bash
python examples/run_from_scenario.py scenarios/baseline_watershed.json
```

Or from Python:

```python
from pathlib import Path

from shrine.simulation import load_and_run

scenario = Path("scenarios/baseline_watershed.json")
result = load_and_run(lambda: model, scenario)

print(result.metadata["status"])
print(result.outputs.head())
```

## 3. Run with explicit inputs (no scenario file)

For a minimal programmatic run:

```python
from shrine.simulation import (
    Clock,
    ConstantInput,
    InputManager,
    Model,
    RunController,
    WatershedElement,
)
from hydrology.watershed import Watershed

ws = Watershed()
ws.add_junction("J1", "sink")
ws.link_catchment("C1", "J1")

model = Model(clock=Clock("1/1/2019", "1/15/2019"))
model.register_watershed("basin", WatershedElement(ws, element_id="basin"))

inputs = InputManager()
inputs.bind("precipitation", ConstantInput(10.0))
inputs.bind("evaporation", ConstantInput(1.0))

result = RunController(model, input_manager=inputs, seed=42).run()
print(result.outputs[["basin.outflow"]].head())
```

## 4. Inspect outputs

`RunResult.outputs` is a wide `pandas` DataFrame — one column per recorded variable, one row per timestep. Run metadata (seed, timestamps, manifest) is on `result.metadata`.

```python
assert result.success
print(result.manifest["elements"])
print(result.outputs.columns.tolist())
```

## 5. Try other examples

From the repo root with your venv activated:

| Script | What it demonstrates |
|--------|----------------------|
| `examples/tutorial_watershed.py` | **Tutorial:** scenario + plot (see [First watershed model](tutorial/first-watershed-model.md)) |
| `examples/watershed_run.py` | Two catchments → junction → flow solve |
| `examples/catchment_run.py` | Single catchment, rational runoff |
| `examples/climate_loop.py` | Framework inputs without Excel |
| `examples/step_debug.py` | Single-timestep `RunController.step()` |
| `examples/custom_element.py` | Minimal custom `Simulatable` element |

## Next steps

- [Tutorial: first watershed model](tutorial/first-watershed-model.md) — scenario + plot (**recommended**)
- [Concepts](concepts.md) — run loop, elements, inputs, recording
- [Scenarios](scenarios.md) — YAML/JSON format and overrides
- [Architecture](architecture.md) — framework vs domain vs adapters
