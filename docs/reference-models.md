# Reference models

Curated **reference scenarios** under [`scenarios/reference/`](https://github.com/jlillywh/SHRINE/tree/master/scenarios/reference) support regression testing, reproducible examples, and future cross-tool comparison. Each case pairs:

1. A **scenario file** (clock + climate inputs)
2. A **model topology** in Python ([`tests/reference/models.py`](https://github.com/jlillywh/SHRINE/blob/master/tests/reference/models.py))
3. A **golden output hash** ([`tests/golden/reference/`](https://github.com/jlillywh/SHRINE/tree/master/tests/golden/reference))

Roadmap item **3.10**.

---

## Catalog

| ID | Scenario | Topology | Notes |
|----|----------|----------|-------|
| **REF-1C** | `synthetic_single_catchment.yaml` | C1 → sink | Minimal end-to-end basin |
| **REF-2C** | `synthetic_twin_catchment.yaml` | C1,C2 → J1 → sink | Parallel subcatchments; monthly precip |
| **REF-NJ** | `synthetic_nested_junction.yaml` | C1→J1, C2→J5→J1 | Nested junction routing |
| **REF-4C2J** | `published_dendritic_routing.yaml` | 4 catchments, 2 junctions | Dendritic layout analogous to multi-gauge intercomparison basins ([Reed et al. 2004 MOPEX](https://doi.org/10.1016/j.jhydrol.2004.03.027); [Newman et al. 2017](https://doi.org/10.1029/2017EO075907)) |

Default catchments use the built-in **Rational** runoff model (`RunoffMethod.SIMPLE`, area 1000 m²). The published-style case uses **synthetic constant climate**, not MOPEX forcing or calibrated parameters — it exercises **network routing** on a layout common in hydrologic intercomparison studies.

---

## Run a reference case

```bash
bash scripts/bootstrap_venv.sh
.venv/bin/python3 -m pip install -e ".[dev]"

# By stem name (default: synthetic_twin_catchment)
.venv/bin/python3 examples/run_reference_scenario.py synthetic_twin_catchment

# Or with load_and_run in your own script — see tests/reference/models.py
```

---

## Regression tests

CI runs golden-hash checks via `tests/simulation/test_reference_run.py`:

- Median timing is **not** checked here (see [benchmark scenario](testing.md#performance-benchmark-roadmap-39) in **3.9**).
- Each case also asserts **day-one routed outflow** against the analytical Rational runoff total where applicable.

Refresh hashes after intentional output changes:

```bash
.venv/bin/python3 scripts/update_reference_golden.py
```

Commit updated files under `tests/golden/reference/` with the PR.

---

## Adding a reference case

1. Add `scenarios/reference/your_case.yaml` with `metadata.reference_id`.
2. Add a builder in `tests/reference/models.py`.
3. Register the case in `tests/reference/manifest.py` (optional `expected_first_outflow` spot check).
4. Run `scripts/update_reference_golden.py` and commit the new `.sha256` file.
5. Document the row in `scenarios/reference/README.md` and this page.

---

## Clone vs PyPI

Reference scenarios ship with the **Git repository** only. After `pip install shrine` from PyPI, clone the repo or copy scenario YAML into your project. See [Install](install.md).
