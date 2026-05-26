#!/usr/bin/env bash
# Run gitleaks against the working tree (full repo). Requires gitleaks on PATH.
# Install: https://github.com/gitleaks/gitleaks#installing
# Or use: pre-commit run gitleaks --all-files

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v gitleaks >/dev/null 2>&1; then
  echo "gitleaks not found. Install from https://github.com/gitleaks/gitleaks/releases" >&2
  echo "Or: pip install pre-commit && pre-commit run gitleaks --all-files" >&2
  exit 1
fi

gitleaks detect --source . --config .gitleaks.toml --verbose --no-git
echo "No secrets detected."
