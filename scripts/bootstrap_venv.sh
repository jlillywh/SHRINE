#!/usr/bin/env bash
# Create or repair the project venv and install dependencies (Ubuntu PEP 668 safe).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VENV_PY="$ROOT/.venv/bin/python3"

if [ ! -x "$VENV_PY" ]; then
  echo "Creating $ROOT/.venv ..."
  python3 -m venv "$ROOT/.venv"
fi

echo "Using: $VENV_PY"
"$VENV_PY" -m pip install -U pip
"$VENV_PY" -m pip install -e ".[dev]"
"$VENV_PY" -c "import pint; print('pint', pint.__version__)"

echo "Done. Run tests with:"
echo "  $VENV_PY -m pytest tests/simulation -v"
