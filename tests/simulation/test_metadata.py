"""Run metadata and reproducible seeds (SCN-03, INP-04, NFR-02)."""

from __future__ import annotations

from shrine.simulation import (
    Clock,
    InputManager,
    Model,
    RunController,
    StochasticInput,
)
from shrine.simulation.metadata import build_run_metadata, enrich_run_metadata
from shrine.simulation.rng import make_rng


class _CounterElement:
    element_type = "counter"

    def __init__(self) -> None:
        self.n = 0

    def initialize(self, run_context) -> None:
        self.n = 0

    def update(self, timestep_context) -> None:
        self.n += 1

    def finalize(self, run_context) -> None:
        pass


class _NoiseRecorder:
    element_type = "noise"

    def __init__(self) -> None:
        self.values: list[float] = []

    def initialize(self, run_context) -> None:
        self.values = []

    def update(self, timestep_context) -> None:
        self.values.append(float(timestep_context.inputs["noise"]))

    def finalize(self, run_context) -> None:
        pass


class TestRunMetadata:
    def test_build_run_metadata_fields(self) -> None:
        model = Model(name="Basin", clock=Clock("1/1/2019", "1/5/2019"))
        meta = build_run_metadata(model, scenario_name="s1", seed=7)
        assert meta["model_name"] == "Basin"
        assert meta["scenario_name"] == "s1"
        assert meta["seed"] == 7
        assert meta["reproducible"] is True
        assert meta["num_timesteps"] == 5
        assert "run_id" in meta
        assert "python_version" in meta

    def test_enrich_adds_framework_fields(self) -> None:
        meta = enrich_run_metadata({"seed": 1})
        assert meta["framework_version"] == "0.2.0"
        assert "run_timestamp_utc" in meta

    def test_run_result_metadata(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("c1", _CounterElement())
        result = RunController(
            model,
            scenario_name="meta_test",
            seed=42,
            raise_on_error=False,
        ).run()
        assert result.success
        m = result.metadata
        assert m["scenario_name"] == "meta_test"
        assert m["seed"] == 42
        assert m["reproducible"] is True
        assert m["status"] == "success"
        assert m["num_timesteps"] == 3
        assert m["elapsed_seconds"] >= 0.0
        assert "run_id" in m


class TestReproducibleSeeds:
    def test_same_seed_identical_stochastic_outputs(self) -> None:
        clock = Clock("1/1/2019", "1/6/2019")
        inputs = InputManager()
        inputs.bind("noise", StochasticInput("normal", loc=5.0, scale=0.1))

        def run_once() -> list[float]:
            model = Model(clock=clock)
            element = _NoiseRecorder()
            model.register("n", element)
            RunController(model, input_manager=inputs, seed=99, raise_on_error=False).run()
            return element.values

        assert run_once() == run_once()

    def test_different_seeds_differ(self) -> None:
        clock = Clock("1/1/2019", "1/6/2019")
        inputs = InputManager()
        inputs.bind("noise", StochasticInput("uniform", low=0.0, high=1.0))

        def run_with(seed: int) -> list[float]:
            model = Model(clock=clock)
            rec = _NoiseRecorder()
            model.register("n", rec)
            RunController(model, input_manager=inputs, seed=seed, raise_on_error=False).run()
            return rec.values

        assert run_with(1) != run_with(2)

    def test_rerun_gets_new_run_id(self) -> None:
        clock = Clock("1/1/2019", "1/4/2019")
        inputs = InputManager()
        inputs.bind("noise", StochasticInput("normal", loc=1.0, scale=0.01))

        def run() -> tuple[str, list[float]]:
            model = Model(clock=clock)
            element = _NoiseRecorder()
            model.register("n", element)
            result = RunController(model, input_manager=inputs, seed=1, raise_on_error=False).run()
            return result.metadata["run_id"], element.values

        id1, v1 = run()
        id2, v2 = run()
        assert id1 != id2
        assert v1 == v2

    def test_make_rng_deterministic(self) -> None:
        a = make_rng(42).normal(0, 1, 3)
        b = make_rng(42).normal(0, 1, 3)
        assert (a == b).all()
