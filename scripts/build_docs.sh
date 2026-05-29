#!/usr/bin/env bash
# Build the MkDocs site locally (roadmap 3.1).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -x .venv/bin/python3 ]]; then
  bash scripts/bootstrap_venv.sh
fi

.venv/bin/python3 -m pip install -q -e ".[docs]"
.venv/bin/python3 scripts/gen_api_reference.py
.venv/bin/mkdocs build --strict "$@"

echo "Site written to site/ — open with: .venv/bin/mkdocs serve"
