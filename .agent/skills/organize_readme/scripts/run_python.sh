#!/usr/bin/env bash
set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Usage: bash .agent/skills/organize_readme/scripts/run_python.sh <script.py> [args...]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
REQ_FILE="${REPO_ROOT}/requirements.txt"

if [[ -d "${HOME:-}/.local/bin" && ":${PATH}:" != *":${HOME}/.local/bin:"* ]]; then
  export PATH="${HOME}/.local/bin:${PATH}"
fi

export PYTHONDONTWRITEBYTECODE=1
export UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/uv-cache}"
export UV_PYTHON_INSTALL_DIR="${UV_PYTHON_INSTALL_DIR:-/tmp/uv-python}"
export UV_TOOL_DIR="${UV_TOOL_DIR:-/tmp/uv-tools}"
export UV_PYTHON_PREFERENCE="${UV_PYTHON_PREFERENCE:-only-system}"

# Resolve optional Python dependencies via uv first, falling back to pip if needed.
if [[ -f "$REQ_FILE" ]] && grep -Eqv '^\s*(#|$)' "$REQ_FILE"; then
  if command -v uv >/dev/null 2>&1; then
    if [[ -d "${REPO_ROOT}/.venv" ]]; then
      uv pip install --quiet --python "${REPO_ROOT}/.venv/bin/python" -r "$REQ_FILE" \
        || python3 -m pip install --quiet -r "$REQ_FILE"
    else
      uv pip install --quiet --system -r "$REQ_FILE" \
        || python3 -m pip install --quiet -r "$REQ_FILE"
    fi
  else
    python3 -m pip install --quiet -r "$REQ_FILE"
  fi
fi

if command -v uv >/dev/null 2>&1; then
  if [[ -d "${REPO_ROOT}/.venv" ]]; then
    exec uv run --no-project --python "${REPO_ROOT}/.venv/bin/python" python3 -B "$@"
  fi
  exec uv run --no-project python3 -B "$@"
fi

exec python3 -B "$@"
