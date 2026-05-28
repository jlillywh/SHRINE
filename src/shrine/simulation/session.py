"""Step-mode session context manager (RUN-04, 1.5)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from shrine.simulation.step import StepResult

if TYPE_CHECKING:
    from shrine.simulation.run_controller import RunController, RunResult


class RunSession:
    """Context manager wrapping ``begin()`` / ``step()`` / ``complete()`` (1.5).

    Example::

        with RunSession(controller) as session:
            for step in session:
                print(step.current_time, step.inputs)
        result = session.result
    """

    def __init__(self, controller: RunController) -> None:
        self.controller = controller
        self.result: RunResult | None = None

    def __enter__(self) -> RunSession:
        self.result = None
        self.controller.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.controller.is_initialized:
            if exc_type is None:
                self.result = self.controller.complete()
            else:
                self.controller.finalize()
        return False

    def __iter__(self) -> Iterator[StepResult]:
        while True:
            step = self.step()
            if step is None:
                return
            yield step

    def step(self) -> StepResult | None:
        """Advance one timestep (delegates to the controller)."""
        return self.controller.step()

    def step_many(self, count: int) -> list[StepResult]:
        """Advance up to ``count`` timesteps."""
        return self.controller.step_many(count)
