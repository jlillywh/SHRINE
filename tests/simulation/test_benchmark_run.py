"""Performance benchmark: fixed scenario → wall-clock regression guard (roadmap 3.9)."""

from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
from typing import Any

import pytest

from shrine.simulation import load_scenario_file, run_scenario
from tests.benchmark.model import build_benchmark_watershed_model
from tests.path_fixtures import REPO_ROOT

BENCHMARK_DIR = Path(__file__).resolve().parent.parent / "benchmark"
TIMING_FILE = BENCHMARK_DIR / "benchmark_watershed.timing.json"


def _load_timing_config() -> dict[str, Any]:
    assert TIMING_FILE.is_file(), f"missing timing config: {TIMING_FILE}"
    return json.loads(TIMING_FILE.read_text(encoding="utf-8"))


def _run_benchmark_once(scenario_path: Path) -> float:
    scenario = load_scenario_file(scenario_path)
    model = build_benchmark_watershed_model()
    start = time.perf_counter()
    result = run_scenario(model, scenario, raise_on_error=False)
    elapsed = time.perf_counter() - start
    assert result.success, result.error
    assert len(result.outputs) >= 360, "benchmark should produce ~365 daily rows"
    return elapsed


@pytest.mark.benchmark
class TestBenchmarkRun:
    def test_benchmark_watershed_within_threshold(self) -> None:
        cfg = _load_timing_config()
        scenario_path = REPO_ROOT / cfg["scenario"]
        assert scenario_path.is_file(), f"missing scenario: {scenario_path}"

        repeats = int(cfg.get("repeats", 3))
        _run_benchmark_once(scenario_path)  # warmup
        samples = [_run_benchmark_once(scenario_path) for _ in range(repeats)]
        elapsed = statistics.median(samples)

        baseline = float(cfg["baseline_seconds"])
        ratio_limit = float(cfg.get("max_regression_ratio", 1.5))
        limit = baseline * ratio_limit

        assert elapsed <= limit, (
            f"benchmark slower than threshold: median {elapsed:.3f}s "
            f"(samples {samples}) > {limit:.3f}s "
            f"(baseline {baseline:.3f}s × {ratio_limit}). "
            "If intentional, run: python scripts/update_benchmark_baseline.py"
        )
