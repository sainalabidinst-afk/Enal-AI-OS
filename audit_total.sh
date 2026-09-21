#!/usr/bin/env bash
set -euo pipefail

echo "=== 1) Setup environment ==="
PYTHON_BIN=""
for candidate in python3 python py; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" --version >/dev/null 2>&1; then
    PYTHON_BIN=$(command -v "$candidate")
    break
  fi
done
if [ -z "$PYTHON_BIN" ]; then
  echo "Python tidak ditemukan. Install python3 lalu jalankan lagi."
  exit 1
fi

"$PYTHON_BIN" -m venv .venv || true
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  source .venv/Scripts/activate
else
  echo "Virtual environment gagal dibuat."
  exit 1
fi
"$PYTHON_BIN" -m pip install -q -U pip setuptools wheel

echo "=== 2) Install dependencies ==="
if [ -f pyproject.toml ]; then
  if [ "${RUN_POETRY_INSTALL:-0}" = "1" ]; then
    "$PYTHON_BIN" -m pip install poetry || true
  fi
  if [ "${RUN_POETRY_INSTALL:-0}" = "1" ] && command -v poetry >/dev/null 2>&1; then
    poetry install --no-interaction --no-ansi || true
  fi
fi
if [ -f requirements.txt ]; then
  "$PYTHON_BIN" -m pip install -r requirements.txt || true
fi

echo "=== 3) Install audit tools ==="
"$PYTHON_BIN" -m pip install -q pytest pytest-cov flake8 black isort bandit safety || true

echo "=== 4) Run tests with coverage ==="
mkdir -p audit_output
pytest --maxfail=1 --disable-warnings --cov=./ --cov-report=term-missing \
  --junitxml=audit_output/junit.xml > audit_output/pytest.txt 2>&1 || true

echo "=== 5) Run linters ==="
flake8 . > audit_output/flake8.txt || true
black --check . > audit_output/black.txt || true
isort --check-only . > audit_output/isort.txt || true

echo "=== 6) Security checks ==="
bandit -r . -f txt -o audit_output/bandit.txt || true
safety check --full-report > audit_output/safety.txt || true

echo "=== 7) Collect metadata ==="
git log -n 20 --pretty=format:'%h %ad %s' --date=short > audit_output/git_commits.txt || true
ls -R > audit_output/file_tree.txt

echo "=== 8) Archive results ==="
tar -czf audit_output.tar.gz audit_output

echo "=== Audit selesai ==="
echo "Output: audit_output.tar.gz"