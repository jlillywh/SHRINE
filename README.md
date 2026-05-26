# Aegis

![Athena's aegis](https://upload.wikimedia.org/wikipedia/en/thumb/d/d6/Douriscup_83d40m_Athene_aegisWingedLionessOwl_pythonVomitsJason_fleeceInTree_Vatican.jpg/330px-Douriscup_83d40m_Athene_aegisWingedLionessOwl_pythonVomitsJason_fleeceInTree_Vatican.jpg)

Integrated water-resources modeling library (Python). Aegis combines legacy domain modules (hydrology, storage, flow networks) with a new **`aegis.simulation`** framework for calendar-driven runs, mass balance, scenario files, and structured outputs.

## Simulation framework (`aegis.simulation`)

The framework is the supported path for headless model runs and tests:

- **`Model`** — register elements (watersheds, reservoirs, custom types) with a shared `Clock`
- **`RunController`** — validate → initialize → timestep loop → finalize
- **`InputManager`** — constant, monthly, and stochastic inputs bound by name
- **`Recorder`** — wide `pandas` DataFrame outputs per run
- **Scenarios** — YAML/JSON clock, inputs, and parameter overrides
- **Flow solve** — NetworkX max-flow on graphs owned by `Watershed` adapters
- **Mass balance** — per-timestep verification with `SimulationError` diagnostics

Requirements and phased delivery: [docs/simulation-framework-requirements.md](docs/simulation-framework-requirements.md).

## Project layout

| Area | Description |
|------|-------------|
| `aegis/simulation/` | Framework: clock, model, run controller, inputs, recorder, scenarios |
| `hydrology/` | Catchments, watersheds, networks |
| `water_manage/` | Storage, flow networks, operating rules |
| `inputs/` | Tables, time series, data helpers |
| `results/` | `TimeHistory` (wraps `Recorder`), charts |
| `examples/` | Runnable demos (climate, watershed, scenarios, stepping) |
| `tests/simulation/` | Framework unit and acceptance tests |
| `docs/` | Guides (see below) |

## Prerequisites

- Python **3.10+**
- WSL/Linux or Windows with WSL recommended for `./scripts/run_tests.sh`

## Install

```bash
cd Aegis
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Optional plotting (legacy charts, `flow_network.draw`):

```bash
pip install -e ".[dev,viz]"
```

## Run tests

```bash
./scripts/run_tests.sh
```

Or manually:

```bash
pytest tests/ -v
pytest tests/simulation --cov=aegis.simulation --cov-report=term-missing
```

See [docs/testing.md](docs/testing.md) for layout and troubleshooting (WSL sync, venv, etc.).

## Secrets and credentials

Do **not** commit API keys or `.env` files. Use `GOOGLE_MAPS_API_KEY` for the optional Maps demo, or a local gitignored `data_external/apikey.txt` (see `data_external/apikey.txt.example`). Full guidance: **[docs/secrets-and-repo-hygiene.md](docs/secrets-and-repo-hygiene.md)**. Optional local hook: `pip install -e ".[dev]" && pre-commit install` (gitleaks on commit); CI runs the same scan on push/PR.

## Examples

From the repo root with the venv activated:

```bash
# Climate inputs via framework (no Excel)
python examples/climate_loop.py

# Two catchments → junction → flow solve
python examples/watershed_run.py

# Scenario file (JSON/YAML)
python examples/run_from_scenario.py scenarios/baseline_watershed.json

# Single-timestep debugging
python examples/step_debug.py

# Minimal custom element
python examples/custom_element.py
```

Bundled scenarios: `scenarios/baseline_watershed.json`, `scenarios/wet_year.yaml`.

## Documentation

| Guide | Topic |
|-------|--------|
| [docs/modernization-roadmap.md](docs/modernization-roadmap.md) | Strategic checklist: pythonic OOP, OSS excellence |
| [docs/simulation-framework-requirements.md](docs/simulation-framework-requirements.md) | Architecture decisions and requirements |
| [docs/extending-elements.md](docs/extending-elements.md) | Adding new `Simulatable` elements |
| [docs/scenarios.md](docs/scenarios.md) | Scenario YAML/JSON |
| [docs/step-debugging.md](docs/step-debugging.md) | `RunController.step()` API |
| [docs/results-recording.md](docs/results-recording.md) | `Recorder` and `TimeHistory` |
| [docs/testing.md](docs/testing.md) | Test suite and CI-style local runs |
| [docs/secrets-and-repo-hygiene.md](docs/secrets-and-repo-hygiene.md) | API keys, `.env`, history purge if a secret was committed |

## Quick API sketch

```python
from aegis.simulation import (
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
print(result.outputs.head())
```

Legacy scripts (e.g. `global_attributes/test_model.py`) remain for reference; prefer `examples/climate_loop.py` and the framework APIs for new work.

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
