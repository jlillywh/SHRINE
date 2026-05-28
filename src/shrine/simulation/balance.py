"""Mass balance verification (MB-*, D5). Phase 1+."""

from __future__ import annotations

from dataclasses import dataclass, field

from shrine.simulation.errors import SimulationError, SimulationPhase


@dataclass
class MassBalanceTerm:
    name: str
    value: float


@dataclass
class MassBalanceReport:
    """Per-timestep balance check result."""

    passed: bool
    residual: float
    tolerance: float
    terms: list[MassBalanceTerm] = field(default_factory=list)


class MassBalanceCheck:
    """Verifies model-wide mass balance each timestep."""

    def __init__(self, tolerance: float = 1e-6) -> None:
        self.tolerance = tolerance

    def verify(self, terms: list[MassBalanceTerm]) -> MassBalanceReport:
        total = sum(t.value for t in terms)
        passed = abs(total) <= self.tolerance
        return MassBalanceReport(
            passed=passed,
            residual=total,
            tolerance=self.tolerance,
            terms=terms,
        )

    def verify_or_raise(
        self,
        terms: list[MassBalanceTerm],
        *,
        step_index: int | None = None,
        timestamp: object = None,
    ) -> MassBalanceReport:
        report = self.verify(terms)
        if not report.passed:
            raise SimulationError(
                message=f"Mass balance violation: residual={report.residual}",
                phase=SimulationPhase.BALANCE,
                step_index=step_index,
                timestamp=timestamp,
                details={"terms": [(t.name, t.value) for t in terms]},
            )
        return report
