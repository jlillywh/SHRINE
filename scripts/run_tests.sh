#!/usr/bin/env bash
# Run simulation framework tests with optional coverage.
# Uses a project .venv (Ubuntu/Debian block system-wide pip via PEP 668).
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -z "${VIRTUAL_ENV:-}" ]; then
  if [ -f .venv/bin/activate ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
  elif [ -f venv/bin/activate ]; then
    # shellcheck source=/dev/null
    source venv/bin/activate
  else
    echo "Creating .venv ..."
    python3 -m venv .venv
    # shellcheck source=/dev/null
    source .venv/bin/activate
  fi
fi

python -m pip install -U pip -q
python -m pip install -e ".[dev]" -q
python -m pytest tests/simulation "$@"
