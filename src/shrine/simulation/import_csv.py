"""Load time-series inputs from CSV (roadmap 3.14)."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import pandas as pd

from shrine.simulation.errors import SimulationError, SimulationPhase
from shrine.simulation.inputs import InputManager, InputProvider, TimeSeriesCsvInput

DEFAULT_TIME_COLUMN = "time"


def resolve_csv_path(path: str | Path, *, base_dir: Path | None = None) -> Path:
    """Resolve *path* relative to *base_dir* (scenario file directory) when not absolute."""
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    root = base_dir if base_dir is not None else Path.cwd()
    return (root / candidate).resolve()


def read_csv_timeseries(path: str | Path) -> pd.DataFrame:
    """Read a CSV file; raises :class:`SimulationError` when missing or empty."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise SimulationError(
            message=f"CSV file not found: {csv_path}",
            phase=SimulationPhase.VALIDATE,
            details={"path": str(csv_path)},
        )
    frame = pd.read_csv(csv_path)
    if frame.empty:
        raise SimulationError(
            message=f"CSV file is empty: {csv_path}",
            phase=SimulationPhase.VALIDATE,
            details={"path": str(csv_path)},
        )
    return frame


def series_from_csv(
    path: str | Path,
    *,
    time_column: str = DEFAULT_TIME_COLUMN,
    value_column: str,
) -> pd.Series:
    """Return a float series indexed by parsed timestamps."""
    frame = read_csv_timeseries(path)
    if time_column not in frame.columns:
        raise SimulationError(
            message=f"CSV missing time column {time_column!r}",
            phase=SimulationPhase.VALIDATE,
            details={"path": str(path), "columns": list(frame.columns)},
        )
    if value_column not in frame.columns:
        raise SimulationError(
            message=f"CSV missing value column {value_column!r}",
            phase=SimulationPhase.VALIDATE,
            details={"path": str(path), "columns": list(frame.columns)},
        )
    series = frame.set_index(time_column)[value_column]
    series.index = pd.to_datetime(series.index)
    return cast(pd.Series, series.astype(float))


def load_csv_timeseries(
    path: str | Path,
    *,
    time_column: str = DEFAULT_TIME_COLUMN,
    value_column: str,
) -> TimeSeriesCsvInput:
    """Load one CSV column as a :class:`TimeSeriesCsvInput`."""
    return TimeSeriesCsvInput(
        series_from_csv(path, time_column=time_column, value_column=value_column)
    )


def bind_csv_columns(
    manager: InputManager,
    path: str | Path,
    column_mapping: dict[str, str],
    *,
    time_column: str = DEFAULT_TIME_COLUMN,
    base_dir: Path | None = None,
) -> None:
    """Bind multiple inputs from one CSV using ``input_name -> column_name`` mapping."""
    for input_name, provider in providers_from_csv_mapping(
        path,
        column_mapping,
        time_column=time_column,
        base_dir=base_dir,
    ).items():
        manager.bind(input_name, provider)


def providers_from_csv_mapping(
    path: str | Path,
    column_mapping: dict[str, str],
    *,
    time_column: str = DEFAULT_TIME_COLUMN,
    base_dir: Path | None = None,
) -> dict[str, InputProvider]:
    """Build input providers from one CSV file and a column mapping."""
    csv_path = resolve_csv_path(path, base_dir=base_dir)
    frame = read_csv_timeseries(csv_path)
    if time_column not in frame.columns:
        raise SimulationError(
            message=f"CSV missing time column {time_column!r}",
            phase=SimulationPhase.VALIDATE,
            details={"path": str(csv_path), "columns": list(frame.columns)},
        )
    indexed = frame.set_index(time_column)
    indexed.index = pd.to_datetime(indexed.index)
    providers: dict[str, InputProvider] = {}
    for input_name, column in column_mapping.items():
        if column not in indexed.columns:
            raise SimulationError(
                message=f"CSV missing mapped column {column!r} for input {input_name!r}",
                phase=SimulationPhase.VALIDATE,
                details={"path": str(csv_path), "input": input_name, "column": column},
            )
        providers[input_name] = TimeSeriesCsvInput(indexed[column].astype(float))
    return providers
