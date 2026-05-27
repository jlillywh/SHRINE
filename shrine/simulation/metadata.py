"""Run metadata helpers (SCN-03, RUN-03)."""

from __future__ import annotations

import sys
import uuid
from datetime import datetime, timezone
from time import perf_counter
from typing import TYPE_CHECKING, Any

from shrine import __version__ as SHRINE_VERSION

if TYPE_CHECKING:
    from shrine.simulation.model import Model
    from shrine.simulation.scenario import ScenarioConfig


def build_run_metadata(
    model: Model,
    *,
    scenario_name: str | None = None,
    seed: int | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Core metadata fields recorded at the start of every run."""
    clock = model.clock
    return {
        "run_id": run_id or str(uuid.uuid4()),
        "model_name": model.name,
        "scenario_name": scenario_name,
        "seed": seed,
        "reproducible": seed is not None,
        "start": str(clock.start_date),
        "end": str(clock.end_date),
        "time_step": str(clock.time_step),
        "num_timesteps": len(clock.range),
        "python_version": sys.version.split()[0],
    }


def enrich_run_metadata(
    metadata: dict[str, Any],
    *,
    scenario: ScenarioConfig | None = None,
    elapsed_seconds: float | None = None,
    status: str | None = None,
) -> dict[str, Any]:
    """Add framework version, UTC timestamp, and optional run outcome fields."""
    metadata = dict(metadata)
    metadata["framework_version"] = SHRINE_VERSION
    metadata["run_timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    if scenario is not None:
        metadata["scenario_name"] = scenario.name
        metadata["seed"] = scenario.seed
        metadata["reproducible"] = scenario.seed is not None
        if scenario.metadata:
            metadata["scenario_metadata"] = scenario.metadata
    if elapsed_seconds is not None:
        metadata["elapsed_seconds"] = round(elapsed_seconds, 6)
    if status is not None:
        metadata["status"] = status
    return metadata


class RunTimer:
    """Simple wall-clock timer for run duration metadata."""

    def __init__(self) -> None:
        self._start = perf_counter()

    def elapsed(self) -> float:
        return perf_counter() - self._start
