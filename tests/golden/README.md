# Golden output hashes

Regression digests for `result.outputs` from fixed scenario files under `scenarios/`.

| Scenario | Hash file |
|----------|-----------|
| `baseline_watershed.json` | `baseline_watershed.outputs.sha256` |

Regenerate after intentional output changes:

```bash
.venv/bin/python3 scripts/update_golden_outputs.py
```

Tests: `tests/simulation/test_golden_run.py`
