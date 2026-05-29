# API reference

The **stable public API** for new SHRINE applications is **`shrine.simulation`**. Import symbols from the package root:

```python
from shrine.simulation import Model, RunController, Clock
```

Do **not** depend on undocumented submodule paths (`shrine.simulation.run_controller`, etc.) unless noted in [Extending elements](../extending-elements.md).

## Versioning

| Symbol | Meaning |
|--------|---------|
| `shrine.__version__` | Package / distribution version |
| `shrine.simulation.__api_version__` | Simulation API contract (currently **1.0**) |

Deprecation rules and SemVer policy: [API stability](../api-stability.md).

## Documented modules

| Page | Scope |
|------|-------|
| [shrine.simulation](simulation.md) | Run orchestration, elements, inputs, flow, scenarios, errors |

Domain packages (`hydrology`, `water_manage`, …) are legacy modules with evolving contracts. Prefer adapters and framework types for new code. Domain protocols are described in [Hydrology contracts](../hydrology-contracts.md).

## Auto-generated docs

API pages use [mkdocstrings](https://mkdocstrings.github.io/) to render docstrings from source. Roadmap item **3.2** will expand coverage and cross-linking; this site already documents the primary `shrine.simulation` entry point.

## Internal symbols

Names prefixed with `_`, modules outside `shrine.simulation.__all__`, and legacy domain packages may change without a deprecation cycle.
