"""Golden-run helpers: stable hashes of scenario outputs for regression tests."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import pandas as pd


def outputs_content_hash(outputs: pd.DataFrame) -> str:
    """SHA-256 hex digest of *outputs* (wide time-indexed DataFrame).

    Canonical form: sorted index and columns, ISO timestamps, JSON array payload.
    """
    if outputs.empty:
        payload: dict[str, Any] = {"columns": [], "index": [], "values": []}
    else:
        frame = outputs.sort_index(axis=0).sort_index(axis=1)
        index = [pd.Timestamp(ts).isoformat() for ts in frame.index]
        columns = [str(c) for c in frame.columns]
        values: list[list[float | None]] = []
        for row in frame.to_numpy():
            row_values: list[float | None] = []
            for cell in row:
                if pd.isna(cell):
                    row_values.append(None)
                else:
                    row_values.append(float(cell))
            values.append(row_values)
        payload = {"columns": columns, "index": index, "values": values}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
