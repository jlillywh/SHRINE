# Reference scenarios (roadmap 3.10)

Curated **synthetic basins** and a **literature-style routing layout** for regression tests, tutorials, and cross-tool comparison. Each scenario pairs with a model topology in `tests/reference/models.py` and a golden output hash under `tests/golden/reference/`.

| Scenario | Topology | Purpose |
|----------|----------|---------|
| [`synthetic_single_catchment.yaml`](synthetic_single_catchment.yaml) | C1 → sink | Minimal end-to-end reference |
| [`synthetic_twin_catchment.yaml`](synthetic_twin_catchment.yaml) | C1,C2 → J1 → sink | Canonical parallel catchments (tutorial-scale) |
| [`synthetic_nested_junction.yaml`](synthetic_nested_junction.yaml) | C1→J1, C2→J5→J1 | Nested junction routing |
| [`published_dendritic_routing.yaml`](published_dendritic_routing.yaml) | 4 catchments, 2 junctions | Dendritic multi-gauge layout (MOPEX / benchmarking style) |

Run a reference case (after `pip install -e ".[dev]"`):

```bash
.venv/bin/python3 examples/run_reference_scenario.py synthetic_twin_catchment
```

See [Reference models](../../docs/reference-models.md) on the doc site.

**Note:** Scenarios live in the Git clone only (not in the PyPI wheel). See [install.md](../../docs/install.md).
