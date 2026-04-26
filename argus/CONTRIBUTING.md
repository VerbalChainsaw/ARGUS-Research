# Contributing to ARGUS-Rerank

Thanks for considering a contribution. **ARGUS-Rerank** (`argus_rerank`) is a small, focused
library and we want to keep it that way. Before opening a PR, please skim
this document and the relevant ARGUS Codex sections.

## Ground rules

1. **DCO sign-off, no CLA.** Every commit must be signed with `git commit -s`.
   This adds a `Signed-off-by` line attesting that you wrote the code or have
   the right to submit it under Apache 2.0. See
   [developercertificate.org](https://developercertificate.org/).
2. **License is Apache 2.0.** Do not relicense, sublicense, or contribute code
   that is incompatible with Apache 2.0.
3. **Scope discipline.** This package is Wedge 1 of the ARGUS architecture. It
   should re-rank documents and emit a calibrated confidence. It should _not_
   become an end-to-end RAG framework, an LLM evaluation harness, or a vector
   store. Scope-creep PRs will be politely closed.
4. **No vendor lock-in.** Optional integrations (MCP, LangChain, LlamaIndex)
   live behind extras and never become required dependencies of the core.

## Getting set up

From a checkout of this repository (the Python package root):

**One command (Windows PowerShell):**

```powershell
.\scripts\dev_setup.ps1
```

**One command (macOS / Linux):**

```bash
./scripts/dev_setup.sh
```

**Or manually:**

```bash
git clone https://github.com/VerbalChainsaw/argus-rerank.git
cd argus-rerank
python -m venv .venv
.venv\Scripts\activate           # Windows
# source .venv/bin/activate      # macOS/Linux
pip install -e ".[dev]"
pytest
```

If you work in the **ARGUS-Research** monorepo (code + PDFs + Codex), open **`ARGUS.code-workspace` at the repository root** (parent of the `argus/` package folder) in Cursor/VS Code. See [docs/WORKSPACE.md](docs/WORKSPACE.md) and the repo root **`AGENTS.md`**.

## What good PRs look like

- A clear problem statement, ideally backed by a benchmark number or a
  reproducible failure case.
- Minimal scope. Touch as few files as possible.
- Tests that demonstrate the behavior change and would have failed before.
- Documentation updates if user-facing behavior changes.
- Conventional commit messages (`feat:`, `fix:`, `docs:`, `refactor:`,
  `test:`, `chore:`) — not required, but appreciated.

## What good PRs do _not_ look like

- Mass reformatting commits.
- Renaming exported types without deprecation.
- Adding new dependencies without justification (see `pyproject.toml`).
- "While I was here, I also..." — split into separate PRs.

## Statement-class discipline

This codebase follows the statement-class taxonomy from ARGUS Codex §3.10. If
you are adding a comment that makes a mathematical or empirical claim, mark it
with one of: `Definition`, `Architecture-conditional proposition`, `Heuristic`,
`Empirical hypothesis`, `Engineering rule`, or `Conjecture`. The word
`theorem` is reserved for statements with actual proof under stated
assumptions; there are currently no theorems in this package.

## Reporting issues

Open a GitHub issue with:
- What you expected
- What actually happened
- A minimal reproduction (input documents + the call you made)
- Your `argus_rerank.__version__` and Python version

For dependence-modeling questions ("should A and B be considered the same
source?"), include both texts and your domain context. We will use those to
expand the typed-edge taxonomy if needed.

## Security

If you find a security issue (e.g., the calibration layer can be tricked into
returning overconfident scores via adversarial input), please email rather
than opening a public issue. Contact details are in `SECURITY.md` (forthcoming).

## Code of conduct

Be civil. Be specific. Be brief. We don't have a formal CoC document yet; the
golden rule is enough until growth makes it not.
