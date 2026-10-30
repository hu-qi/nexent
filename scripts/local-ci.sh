#!/usr/bin/env bash
# Local dry-run of .github/workflows/ci.yml (same steps: install → lint → test).
# Usage: bash scripts/local-ci.sh
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"

echo "==> [1/3] Installing dev toolchain (pytest, ruff)"
"$PYTHON" -m pip install --quiet --upgrade pip
"$PYTHON" -m pip install --quiet -r requirements-dev.txt
"$PYTHON" -m pip install --quiet -e .

echo "==> [2/3] Lint (ruff check .)"
"$PYTHON" -m ruff check .

echo "==> [3/3] Tests (pytest, junit-xml report)"
mkdir -p test-reports
"$PYTHON" -m pytest tests/ -v --junitxml=test-reports/junit.xml

echo "==> OK: lint passed, tests green, report at test-reports/junit.xml"
