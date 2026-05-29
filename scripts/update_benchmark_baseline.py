#!/usr/bin/env python3
"""Refresh benchmark timing baseline under tests/benchmark/."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tests.benchmark.model import build_benchmark_watershed_model  # noqa: E402

from shrine.simulation import load_scenario_file, run_scenario  # noqa: E402

BENCHMARK_DIR = REPO_ROOT / "tests" / "benchmark"
TIMING_FILE = BENCHMARK_DIR / "benchmark_watershed.timing.json"
SCENARIO = REPO_ROOT / "scenarios" / "benchmark" / "benchmark_watershed.yaml"
CALIBRATION_REPEATS = 7
HEADROOM = 1.15

BASELINE_KEYS = {
    "local": "baseline_seconds",
    "ci": "ci_baseline_seconds",
}


def _run_once() -> float:
    scenario = load_scenario_file(SCENARIO)
    model = build_benchmark_watershed_model()
    start = time.perf_counter()
    result = run_scenario(model, scenario, raise_on_error=False)
    elapsed = time.perf_counter() - start
    if not result.success:
        raise RuntimeError(result.error)
    return elapsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=("local", "ci"),
        default="local",
        help="local = dev machine baseline; ci = GitHub Actions ubuntu-latest baseline",
    )
    args = parser.parse_args()

    if not SCENARIO.is_file():
        print(f"missing scenario: {SCENARIO}", file=sys.stderr)
        return 1

    _run_once()  # warmup (cold import / first run)
    samples = [_run_once() for _ in range(CALIBRATION_REPEATS)]
    median = statistics.median(samples)
    baseline = round(median * HEADROOM, 4)

    cfg: dict[str, object] = {}
    if TIMING_FILE.is_file():
        cfg = json.loads(TIMING_FILE.read_text(encoding="utf-8"))

    baseline_key = BASELINE_KEYS[args.target]
    cfg.update(
        {
            "name": "benchmark_watershed",
            "scenario": "scenarios/benchmark/benchmark_watershed.yaml",
            baseline_key: baseline,
            "max_regression_ratio": cfg.get("max_regression_ratio", 1.5),
            "repeats": cfg.get("repeats", 3),
            "notes": (
                "baseline_seconds = local dev median × 1.15; "
                "ci_baseline_seconds = GHA ubuntu-latest median × 1.15"
            ),
        }
    )

    BENCHMARK_DIR.mkdir(parents=True, exist_ok=True)
    TIMING_FILE.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    print(f"target: {args.target} ({baseline_key})")
    print(f"samples (s): {[round(s, 4) for s in samples]}")
    print(f"median: {median:.4f}s → {baseline_key}: {baseline}")
    print(f"wrote {TIMING_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
