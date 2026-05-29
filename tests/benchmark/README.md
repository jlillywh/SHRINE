# Performance benchmark (roadmap 3.9)

Fixed scenario for **wall-clock regression** checks in CI (optional threshold via `max_regression_ratio`).

| File | Purpose |
|------|---------|
| [`benchmark_watershed.timing.json`](benchmark_watershed.timing.json) | Baseline seconds + allowed slowdown ratio |
| [`../scenarios/benchmark/benchmark_watershed.yaml`](../../scenarios/benchmark/benchmark_watershed.yaml) | Scenario: 365 daily steps, twin catchments |

Test: `tests/simulation/test_benchmark_run.py`

## Baselines

GitHub Actions runners are much slower than a typical dev laptop. The timing file stores **two** baselines:

| Key | Used when |
|-----|-----------|
| `baseline_seconds` | Local `pytest` (no `CI` env) |
| `ci_baseline_seconds` | CI (`CI=true`, e.g. GitHub Actions) |

Refresh after intentional perf changes:

```bash
# Local dev machine
.venv/bin/python3 scripts/update_benchmark_baseline.py

# On GitHub Actions ubuntu-latest (or any CI-like runner)
.venv/bin/python3 scripts/update_benchmark_baseline.py --target ci
```

Commit the updated `benchmark_watershed.timing.json` with the PR that changes performance.
