# ARGUS — research + code (monorepo)

One repository for **PRC/ARGUS research** and the **ARGUS-Rerank** implementation so you (and the AI) can read the Codex and PDFs while editing code in the same workspace.

| Path | What |
|------|------|
| **`ARGUS_CODEX.md`** | Master consolidated Codex (split copy also under `argus/docs/codex/`) |
| **`*.pdf`**, **`prc_v11_gap_closure_bundle.zip`** | Strategy, audit, publication, gap materials |
| **`argus/`** | Python package **`argus_rerank`** — PyPI name `argus-rerank`, CLI `argus-rerank` |

## Cursor / VS Code

**Open `ARGUS.code-workspace` in this folder** (repo root). It sets Python paths to `argus/` and keeps research + code in one tree.

- First-time setup: **Run Task** → `argus-rerank: setup (venv + install)` (installs `argus/.venv`), then select that interpreter.
- See `argus/docs/WORKSPACE.md` for tasks and debugging.

## GitHub

This repo is the **single source of truth** for research artifacts and the Argus-Rerank code together.

An earlier standalone clone lived at [`argus-rerank`](https://github.com/VerbalChainsaw/argus-rerank) (history preserved there); new work should land **here**.

## AI / contributors

Read **`AGENTS.md`** for what to consult before changing implementation code.
