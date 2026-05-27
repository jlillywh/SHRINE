#!/usr/bin/env bash
# Remove duplicate legacy aegis/ tree after shrine/ exists (run from repo root).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -d shrine ]]; then
  echo "shrine/ missing — run scripts/rename_to_shrine.sh first" >&2
  exit 1
fi

if [[ -d aegis ]]; then
  echo "Removing legacy aegis/ (shrine/ is canonical)"
  git rm -rf aegis
else
  echo "No aegis/ directory — nothing to remove"
fi
