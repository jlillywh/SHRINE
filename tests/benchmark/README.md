# Performance benchmark (roadmap 3.9)

Fixed scenario for **wall-clock regression** checks in CI (optional threshold via `max_regression_ratio`).

| File | Purpose |
|------|---------|
| [`benchmark_watershed.timing.json`](benchmark_watershed.timing.json) | Baseline seconds + allowed slowdown ratio |
| [`../scenarios/benchmark/benchmark_watershed.yaml`](../../scenarios/benchmark/benchmark_watershed.yaml) | Scenario: 365 daily steps, twin catchments |

Test: `tests/simulation/test_benchmark_run.py`

Refresh baseline after intentional perf changes:

```bash
.venv/bin/python3 scripts/update_benchmark_baseline.py
```

Commit the updated `benchmark_watershed.timing.json` with the PR that changes performance.
