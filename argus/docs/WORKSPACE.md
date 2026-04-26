# Editor workspace (Cursor / VS Code)

## Recommended — monorepo (research + code)

Repository layout:

```text
ARGUS Research/              ← git root: Codex, PDFs, argus/ package
  ARGUS.code-workspace      ← open this
  AGENTS.md
  ARGUS_CODEX.md
  argus/                     ← Python package (argus_rerank)
    .venv/
    src/
    tests/
```

1. **File → Open Workspace from File…** → **`ARGUS.code-workspace`** in the **repo root** (parent of `argus/`), not only the `argus` subfolder.
2. **Run Task** → `argus-rerank: setup (venv + install)` (creates `argus/.venv` and installs the package in editable mode).
3. **Python: Select Interpreter** → `argus\.venv\Scripts\python.exe` (Windows) or `argus/.venv/bin/python` (macOS/Linux).

## Code-only (argus/ folder only)

Open the `argus/` folder. Run `scripts\dev_setup.ps1` (Windows) or `scripts/dev_setup.sh` (Unix), then select `argus/.venv` as the interpreter. Tasks in `argus/.vscode/` assume `${workspaceFolder}` is `argus/`; prefer the monorepo workspace above for research + code.

## Tasks and debug (root workspace)

| Task / launch | Purpose |
|---------------|---------|
| **argus-rerank: setup (venv + install)** | `venv` + `pip install -e ".[dev]"` under `argus/` |
| **argus-rerank: pytest** | Full test suite |
| **argus-rerank: ruff check** | Linter |
| **argus-rerank: mypy** | Type-check `src/argus_rerank` |
| **argus-rerank: demo (ftx_demo)** | Synthetic demo |
| **argus-rerank: pytest (all)** (Run and Debug) | Debug with **debugpy** |

Install recommended extensions when prompted (**Python**, **Ruff**, **debugpy**).

## AI / contributors

Before changing `argus/src/`, read **`AGENTS.md`** at the repo root and **`ARGUS_CODEX.md`**.
