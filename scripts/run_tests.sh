#!/usr/bin/env bash
# Run simulation framework tests with optional coverage.
# Uses a project .venv (Ubuntu/Debian block system-wide pip via PEP 668).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VENV_PY="$ROOT/.venv/bin/python3"

if [ ! -x "$VENV_PY" ]; then
  echo "No .venv found; running scripts/bootstrap_venv.sh ..."
  bash "$ROOT/scripts/bootstrap_venv.sh"
fi

"$VENV_PY" -m pip install -U pip -q
"$VENV_PY" -m pip install -e ".[dev]" -q
"$VENV_PY" -c "import pint" 2>/dev/null || {
  echo "ERROR: pint not installed in .venv. Run: bash scripts/bootstrap_venv.sh" >&2
  exit 1
}
"$VENV_PY" -m pytest tests/simulation "$@"
