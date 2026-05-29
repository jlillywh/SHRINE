#!/usr/bin/env bash
# Build sdist + wheel for PyPI (roadmap 3.6).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -x .venv/bin/python3 ]]; then
  bash scripts/bootstrap_venv.sh
fi

.venv/bin/python3 -m pip install -U pip build
.venv/bin/python3 -m build --outdir dist "$@"
echo "Built dist/ — verify with: .venv/bin/pip install dist/*.whl"
