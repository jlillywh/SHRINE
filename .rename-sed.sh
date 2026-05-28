#!/bin/bash
set -euo pipefail
cd /home/jason/Aegis

FIND_FILES=(find . \( -path ./.git -o -path ./.venv -o -path ./venv \) -prune -o -type f \( -name *.py -o -name *.md -o -name *.toml -o -name *.yml -o -name *.yaml -o -name *.json -o -name *.sh -o -name *.txt \) -print0)

sed_all() {
  local from=shrine.
sed_all import to=aegis import
   | xargs -0 -r sed -i s|||g
}

sed_all aegis\.simulation shrine.simulation
sed_all from
