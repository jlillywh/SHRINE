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

## Auto-generated reference

API pages are built with [mkdocstrings](https://mkdocstrings.github.io/) from **`shrine.simulation` docstrings** (roadmap **3.2**):

1. `scripts/gen_api_reference.py` reads `shrine.simulation.__all__` and writes `docs/api/autogen/*.md`.
2. `mkdocs build` renders Google-style docstrings into HTML.

Regenerate after changing the public API or docstrings:

```bash
pip install -e ".[docs]"
python scripts/gen_api_reference.py
mkdocs build --strict
```

Start at [shrine.simulation](simulation.md) for the package index and links to each section.

## Internal symbols

Names prefixed with `_`, modules outside `shrine.simulation.__all__`, and legacy domain packages may change without a deprecation cycle.

Domain protocols: [Hydrology contracts](../hydrology-contracts.md).
