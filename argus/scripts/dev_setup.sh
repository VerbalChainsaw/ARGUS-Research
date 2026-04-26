#!/usr/bin/env bash
# Create .venv and install ARGUS-Rerank in editable mode with dev dependencies.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> ARGUS-Rerank dev setup (root: $ROOT)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 not found on PATH" >&2
  exit 1
fi

if [[ ! -d .venv ]]; then
  echo "Creating .venv ..."
  python3 -m venv .venv
fi

PY="$ROOT/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "error: expected venv python at $PY" >&2
  exit 1
fi

"$PY" -m pip install --upgrade pip
"$PY" -m pip install -e ".[dev]"

echo ""
echo "Done. In Cursor/VS Code: select interpreter"
echo "  $PY"
echo "Then: Run Task -> argus-rerank: pytest"
