"""Export run results to CSV + JSON manifest (roadmap 3.13)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pandas as pd

from shrine.simulation.run_controller import RunResult

EXPORT_FORMAT_VERSION = "1.0"
DEFAULT_CSV_NAME = "results.csv"
DEFAULT_MANIFEST_NAME = "run_manifest.json"


def outputs_to_csv_frame(outputs: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of *outputs* with a ``time`` column (Excel-friendly strings)."""
    if outputs.empty:
        return pd.DataFrame(columns=["time"])

    frame = outputs.copy()
    if frame.index.name != "time":
        frame = frame.reset_index()
        if "time" not in frame.columns:
            frame = frame.rename(columns={frame.columns[0]: "time"})
    else:
        frame = frame.reset_index()

    time_col = pd.to_datetime(frame["time"])
    if (
        (time_col.dt.hour == 0).all()
        and (time_col.dt.minute == 0).all()
        and (time_col.dt.second == 0).all()
    ):
        frame["time"] = time_col.dt.strftime("%Y-%m-%d")
    else:
        frame["time"] = time_col.dt.strftime("%Y-%m-%d %H:%M:%S")
    return cast(pd.DataFrame, frame)


def build_export_manifest(
    result: RunResult,
    *,
    outputs_file: str = DEFAULT_CSV_NAME,
) -> dict[str, Any]:
    """Sidecar manifest: run provenance plus export metadata."""
    manifest = dict(result.manifest)
    manifest["export_format_version"] = EXPORT_FORMAT_VERSION
    manifest["outputs_file"] = outputs_file
    manifest["outputs_columns"] = [str(column) for column in result.outputs.columns]
    manifest["outputs_row_count"] = int(len(result.outputs))
    if "output_units" not in manifest:
        manifest["output_units"] = {}
    return manifest


def export_run_result(
    result: RunResult,
    directory: str | Path,
    *,
    csv_name: str = DEFAULT_CSV_NAME,
    manifest_name: str = DEFAULT_MANIFEST_NAME,
) -> tuple[Path, Path]:
    """Write CSV outputs and JSON manifest under *directory*.

    Returns ``(csv_path, manifest_path)``. Creates *directory* if needed.
    """
    out_dir = Path(directory)
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / csv_name
    manifest_path = out_dir / manifest_name

    csv_frame = outputs_to_csv_frame(result.outputs)
    csv_frame.to_csv(csv_path, index=False)

    manifest = build_export_manifest(result, outputs_file=csv_name)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return csv_path, manifest_path
