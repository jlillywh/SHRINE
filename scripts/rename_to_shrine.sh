#!/usr/bin/env bash
# Rename Aegis package and references to SHRINE (run from repo root).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Working in $ROOT"

if [[ -d aegis && ! -d shrine ]]; then
  echo "==> git mv aegis -> shrine"
  git mv aegis shrine
elif [[ -d shrine ]]; then
  echo "==> shrine/ already exists"
else
  echo "ERROR: neither shrine/ nor shrine/ found" >&2
  exit 1
fi

if [[ -f data/shrine_units.json && ! -f data/shrine_units.json ]]; then
  git mv data/shrine_units.json data/shrine_units.json
fi

if [[ -f global_attributes/aegis.py && ! -f global_attributes/shrine_object.py ]]; then
  git mv global_attributes/aegis.py global_attributes/shrine_object.py
fi

if [[ -f global_attributes/test_shrine_object.py && ! -f global_attributes/test_shrine_object.py ]]; then
  git mv global_attributes/test_shrine_object.py global_attributes/test_shrine_object.py
fi

# Content replacements in tracked text files
export LC_ALL=C
while IFS= read -r -d '' f; do
  case "$f" in
    ./.git/*|./.venv/*|./venv/*) continue ;;
  esac
  perl -i -pe '
    s/aegis\.simulation/shrine.simulation/g;
    s/from aegis\./from shrine./g;
    s/import shrine\b/import shrine/g;
    s|shrine/|shrine/|g;
    s/shrine_units/shrine_units/g;
    s/global_attributes\.shrine/global_attributes.shrine_object/g;
    s/from global_attributes\.shrine/from global_attributes.shrine_object/g;
    s/\bclass Aegis\b/class ShrineObject/g;
    s/\bAegis\.__init__/ShrineObject.__init__/g;
    s/\(Aegis\)/(ShrineObject)/g;
    s/\bTestAegis\b/TestShrineObject/g;
    s/\btest_aegis\b/test_shrine_object/g;
    s/name = "shrine"/name = "shrine"/g;
    s/\["aegis\*/["shrine*/g;
    s/source = \["aegis"\]/source = ["shrine"]/g;
    s/Integrated water resources modeling \(Aegis\)/SHRINE — Simulation of Hydrology, Reservoirs, and Integrated Network Engine/g;
    s/SHRINE gitleaks/SHRINE gitleaks/g;
  ' "$f" 2>/dev/null || true
done < <(find . -type f \( -name '*.py' -o -name '*.md' -o -name '*.toml' -o -name '*.yml' -o -name '*.yaml' -o -name '*.json' -o -name '*.sh' \) ! -path './.git/*' ! -path './.venv/*' ! -path './venv/*' -print0)

# shrine_object.py docstrings
if [[ -f global_attributes/shrine_object.py ]]; then
  perl -i -pe '
    s/all Aegis objects/all SHRINE objects/g;
    s/Aegis base_unit/SHRINE base_unit/g;
  ' global_attributes/shrine_object.py
fi

echo "==> Remaining shrine/Aegis references (excluding image URLs):"
rg -n '\baegis\b|\bAegis\b' --glob '!.git' --glob '!.venv' --glob '!venv' . 2>/dev/null | rg -v 'wikipedia|Athena' || true

echo "==> Done. Run: pytest tests/simulation -q"
