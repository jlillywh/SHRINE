"""Run manifest on RunResult (1.4)."""

from __future__ import annotations

from shrine.simulation import (
    Clock,
    Model,
    RunController,
    ScenarioConfig,
    scenario_content_hash,
)
from shrine.simulation.manifest import build_run_manifest, resolve_git_commit


class _StubElement:
    element_type = "stub"

    def initialize(self, run_context) -> None:
        pass

    def update(self, timestep_context) -> None:
        pass

    def finalize(self, run_context) -> None:
        pass


def test_run_result_manifest_fields() -> None:
    model = Model(name="Basin", clock=Clock("1/1/2019", "1/5/2019"))
    model.register("basin", _StubElement())
    scenario = ScenarioConfig(
        name="dry",
        seed=42,
        clock={"start_date": "1/1/2019", "end_date": "1/5/2019"},
        inputs={"precipitation": 10.0},
    )
    result = RunController(
        model,
        scenario_name=scenario.name,
        seed=scenario.seed,
        scenario=scenario,
        raise_on_error=False,
    ).run()

    manifest = result.manifest
    assert manifest["run_id"] == result.metadata["run_id"]
    assert manifest["scenario_name"] == "dry"
    assert manifest["seed"] == 42
    assert manifest["reproducible"] is True
    assert manifest["scenario_hash"] == scenario_content_hash(scenario)
    assert manifest["started_at_utc"]
    assert manifest["finished_at_utc"]
    assert manifest["status"] == "success"
    assert manifest["elements"] == [
        {"element_id": "basin", "element_type": "stub"},
    ]
    assert "git_commit" in manifest
    assert manifest is result.metadata["manifest"]


def test_scenario_content_hash_stable() -> None:
    a = ScenarioConfig(name="x", seed=1, inputs={"p": 1.0})
    b = ScenarioConfig(name="x", seed=1, inputs={"p": 1.0})
    c = ScenarioConfig(name="x", seed=2, inputs={"p": 1.0})
    assert scenario_content_hash(a) == scenario_content_hash(b)
    assert scenario_content_hash(a) != scenario_content_hash(c)


def test_resolve_git_commit_in_repo() -> None:
    commit = resolve_git_commit()
    if commit is not None:
        assert len(commit) >= 7
