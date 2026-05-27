"""Tests for RunSession context manager (1.5)."""

from __future__ import annotations

import pytest

from shrine.simulation import Clock, Model, RunController, RunSession


class _CounterElement:
    element_type = "counter"

    def __init__(self) -> None:
        self.total = 0

    def initialize(self, run_context) -> None:
        self.total = 0

    def update(self, timestep_context) -> None:
        self.total += 1

    def finalize(self, run_context) -> None:
        pass


class TestRunSession:
    def test_context_manager_completes_on_exit(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/5/2019"))
        model.register("c1", _CounterElement())
        controller = RunController(model, raise_on_error=False)

        with RunSession(controller) as session:
            steps = list(session)

        assert len(steps) == 5
        assert steps[-1].done is True
        assert session.result is not None
        assert session.result.success is True
        assert session.result.metadata["debug_mode"] is True
        assert session.result.metadata["steps_completed"] == 5
        assert not controller.is_initialized

    def test_controller_session_factory(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("c1", _CounterElement())
        controller = RunController(model, raise_on_error=False)

        with controller.session() as session:
            assert session.controller is controller
            session.step_many(10)

        assert session.result is not None
        assert session.result.manifest["elements"]

    def test_exception_finalizes_without_result(self) -> None:
        model = Model(clock=Clock("1/1/2019", "1/3/2019"))
        model.register("c1", _CounterElement())
        controller = RunController(model, raise_on_error=False)

        with pytest.raises(RuntimeError):
            with RunSession(controller) as session:
                session.step()
                raise RuntimeError("debug stop")

        assert session.result is None
        assert not controller.is_initialized
