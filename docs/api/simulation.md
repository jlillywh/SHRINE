# shrine.simulation

Public simulation framework API (**`__api_version__` = 1.0**). Import symbols from the package root:

```python
import shrine.simulation as sim
from shrine.simulation import Model, RunController
```

## Version symbols

| Symbol | Description |
|--------|-------------|
| `shrine.__version__` | Distribution version (`__framework_version__` in this package) |
| `shrine.simulation.__api_version__` | Stable simulation API contract |

::: shrine.simulation
    options:
      members:
        - __api_version__
        - __framework_version__
      show_submodules: false
      heading_level: 3
      show_root_heading: true
      show_if_no_docstring: true

## API sections

Reference pages below are **auto-generated** from docstrings (`scripts/gen_api_reference.py`):

| Section | Topics |
|---------|--------|
| [Run orchestration](autogen/run-orchestration.md) | `Model`, `RunController`, `RunResult`, … |
| [Time and context](autogen/time-and-context.md) | `Clock`, `RunContext`, `TimestepContext` |
| [Units](autogen/units.md) | `get_unit_registry`, `validate_unit_string`, … |
| [Elements and adapters](autogen/elements.md) | `Simulatable`, `WatershedElement`, … |
| [Inputs](autogen/inputs.md) | `InputManager`, providers |
| [Flow and mass balance](autogen/flow-balance.md) | `FlowSolver`, `MassBalanceCheck`, … |
| [Scenarios and recording](autogen/scenarios.md) | `ScenarioConfig`, `Recorder`, loaders |
| [Metadata, manifest, and RNG](autogen/metadata.md) | Provenance helpers, `make_rng` |
| [Errors and deprecation](autogen/errors.md) | `SimulationError`, `warn_api_deprecated` |

Policy: [API stability](../api-stability.md).
