# ARGUS research materials

This repository holds **PRC/ARGUS research documents** and the **ARGUS Codex** (`ARGUS_CODEX.md`).

- **ARGUS_CODEX.md** — consolidated architecture, audits, decisions, and wedge plans.
- **PDFs** — strategy, publication, and prior-art material referenced by the program.

The **ARGUS-Rerank** implementation (Wedge 1) lives in a **separate** repo: clone [`argus`](https://github.com/VerbalChainsaw/argus-rerank) (see `argus/README.md` when you have that checkout next to this folder).

## Layout (typical)

```text
ARGUS Research/          ← this repo
  ARGUS_CODEX.md
  *.pdf
  WORKSPACE.md
  argus/                 ← not tracked here; its own git repo
```

Open `argus/ARGUS.code-workspace` from the `argus` clone for the multi-root editor layout.
