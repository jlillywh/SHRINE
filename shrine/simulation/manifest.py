"""Run manifest for reproducibility and provenance (RUN-03, 1.4)."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from shrine import __version__ as SHRINE_VERSION

if TYPE_CHECKING:
    from shrine.simulation.model import Model
    from shrine.simulation.scenario import ScenarioConfig

_REPO_ROOT = Path(__file__).resolve().parents[2]


def resolve_git_commit(*, cwd: Path | None = None) -> str | None:
    """Return current ``git rev-parse HEAD``, or ``None`` if unavailable."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=2,
            cwd=cwd or _REPO_ROOT,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    commit = result.stdout.strip()
    return commit or None


def scenario_content_hash(scenario: ScenarioConfig) -> str:
    """Stable SHA-256 of scenario configuration (clock, inputs, overrides, seed)."""
    payload = {
        "name": scenario.name,
        "seed": scenario.seed,
        "clock": scenario.clock,
        "inputs": scenario.inputs,
        "overrides": scenario.overrides,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def hash_file(path: str | Path) -> str:
    """SHA-256 hex digest of a file's raw bytes."""
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()


def element_list_from_model(model: Model) -> list[dict[str, Any]]:
    """Registered elements for the run manifest."""
    entries: list[dict[str, Any]] = []
    for registered in model.elements():
        element_type = getattr(
            registered.element,
            "element_type",
            type(registered.element).__name__,
        )
        entry: dict[str, Any] = {
            "element_id": registered.element_id,
            "element_type": element_type,
        }
        kind = registered.metadata.get("kind")
        if kind:
            entry["kind"] = kind
        entries.append(entry)
    return sorted(entries, key=lambda item: item["element_id"])


def build_run_manifest(
    model: Model,
    metadata: dict[str, Any],
    *,
    scenario: ScenarioConfig | None = None,
    git_commit: str | None | object = ...,
) -> dict[str, Any]:
    """Assemble the structured run manifest attached to :class:`RunResult`."""
    if git_commit is ...:
        commit = resolve_git_commit()
    else:
        commit = git_commit

    scenario_hash: str | None = None
    scenario_source: str | None = None
    scenario_name = metadata.get("scenario_name")
    if scenario is not None:
        scenario_name = scenario.name
        scenario_hash = scenario_content_hash(scenario)
        scenario_source = scenario.metadata.get("source_file")

    manifest: dict[str, Any] = {
        "run_id": metadata.get("run_id"),
        "model_name": metadata.get("model_name", model.name),
        "scenario_name": scenario_name,
        "scenario_hash": scenario_hash,
        "scenario_source_file": scenario_source,
        "seed": metadata.get("seed"),
        "reproducible": metadata.get("reproducible"),
        "git_commit": commit,
        "started_at_utc": metadata.get("started_at_utc"),
        "finished_at_utc": metadata.get("finished_at_utc"),
        "run_timestamp_utc": metadata.get("run_timestamp_utc"),
        "elapsed_seconds": metadata.get("elapsed_seconds"),
        "status": metadata.get("status"),
        "start": metadata.get("start"),
        "end": metadata.get("end"),
        "time_step": metadata.get("time_step"),
        "num_timesteps": metadata.get("num_timesteps"),
        "elements": element_list_from_model(model),
        "framework_version": metadata.get("framework_version", SHRINE_VERSION),
        "python_version": metadata.get("python_version"),
    }
    if scenario is not None and scenario.metadata:
        manifest["scenario_metadata"] = dict(scenario.metadata)
    return manifest
