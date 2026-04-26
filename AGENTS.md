# ARGUS — agent / contributor context

Use this when editing **implementation code** under `argus/` or when research and code must stay aligned.

## Read first (source of truth)

1. **`ARGUS_CODEX.md`** (repo root) — consolidated architecture, defect register, decision log, wedge specs, and bibliography.
2. **`argus/docs/codex/`** — same Codex split into files; easier to grep and link from code reviews.
3. **PDFs / zip in this repo** — strategy and audit context referenced by the Codex and decision log.

## Code location

- **Package:** `argus/src/argus_rerank/`
- **Product name:** ARGUS-Rerank · **import** `argus_rerank` · **pip** `argus-rerank` · **CLI** `argus-rerank`

Do not expand scope into “full ARGUS” inside this package; the Codex defines Wedge 1 as dependence-aware reranking only.

## Statement-class discipline

Follow ARGUS Codex §3.10 for mathematical / empirical claims in docstrings and docs (no casual “theorem” without proof).
