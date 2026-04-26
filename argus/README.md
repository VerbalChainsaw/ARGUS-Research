# ARGUS-Rerank

> **Dependence-aware reranking for retrieval-augmented generation.**  
> PyPI / CLI: `argus-rerank` · Python import: `argus_rerank` · Part of the broader **ARGUS** program.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](#status)

**ARGUS-Rerank** is a small, focused library that fixes a real problem in
retrieval-augmented generation: **most retrieved passages are not independent
sources.** They quote, summarize, mirror, share authors, share threads, or are
generated from each other. Vanilla RAG counts them all the same.

> _47 documents say the same thing. Three of them know it firsthand. The other 44
> are echoes._

It takes a query and a candidate set of retrieved documents,
constructs a typed dependence graph, computes an **effective corroboration
count** `C_eff` that discounts correlated evidence, and produces a re-ranked
list with a calibrated confidence on the underlying claim.

It is the first wedge of the ARGUS / PRC architecture (see
[`docs/codex/`](docs/codex/) for the full constitution). It is
designed to ship and stand on its own — you do not need to adopt anything else
from ARGUS to use it.

## Why this exists

Every published RAG framework treats retrieved passages as conditionally
independent given the query. That assumption is convenient and usually wrong.
The truth-discovery literature (Yin 2008, Dong 2009, Pochampally 2014) solved
the dependence-modeling problem decades ago for the structured-data case.
ARGUS-Rerank brings that lineage to LLM-era RAG.

The named primitive is **dependence-aware corroboration**. The contribution is
small, mechanical, and easy to ablate.

## Install

```bash
pip install argus-rerank
```

(Once published. For now, install from source — see [Development](#development).)

## 30-second quickstart

```python
from argus_rerank import DependenceAwareReranker, Document

reranker = DependenceAwareReranker()

documents = [
    Document(id="d1", text="FTX customer funds were not segregated from Alameda's accounts.",
             source="WSJ", author="reporter_a", timestamp="2022-11-09"),
    Document(id="d2", text="FTX customer funds were not segregated from Alameda's accounts.",
             source="Bloomberg", author="reporter_b", timestamp="2022-11-09"),
    Document(id="d3", text="According to a WSJ report, FTX customer funds were not segregated.",
             source="Reuters", author="reporter_c", timestamp="2022-11-10"),
    Document(id="d4", text="Internal memo confirms commingling of customer balances.",
             source="court_filing", author="trustee", timestamp="2022-12-15"),
]

result = reranker.rerank(
    query="Were FTX customer funds segregated from Alameda?",
    documents=documents,
)

print(f"Naive corroboration count:        {result.naive_count}")
print(f"Effective independent sources:    {result.effective_n:.2f}")
print(f"Calibrated claim confidence:      {result.confidence:.2f}")

for ranked in result.ranked_documents:
    print(f"  {ranked.document.id:>4}  weight={ranked.weight:.2f}  "
          f"reason={ranked.dependence_summary}")
```

What this prints (illustrative — exact numbers depend on configuration):

```
Naive corroboration count:        4
Effective independent sources:    2.31
Calibrated claim confidence:      0.74

  d4    weight=1.00   reason=independent
  d1    weight=0.95   reason=independent (primary)
  d2    weight=0.42   reason=mirrors d1 (near-duplicate)
  d3    weight=0.30   reason=quote-of d1 (attributed paraphrase)
```

## What ARGUS-Rerank does

| Stage | What happens |
|---|---|
| **1. Near-duplicate detection** | SimHash + MinHash with configurable thresholds; finds documents that are textually mirrored. |
| **2. Citation-graph collapse** | Builds a typed dependence DAG using the V12 §10 edge taxonomy: `derived-from`, `mirrors`, `summary-of`, `quote-of`, `same-author-same-event`, `same-thread`, `same-ticket`, `same-generated-summary`. |
| **3. Copy-language detection** | n-gram overlap + optional LLM-as-judge fallback for paraphrase cases the surface heuristics miss. |
| **4. Effective corroboration `C_eff`** | Computes `C_eff(c) = Σ uᵢ − Σ δᵢⱼ` per ARGUS Codex §3.6, with logarithmic saturation damping so a thousand mirrors of one source cannot dominate three independent ones. |
| **5. Calibrated confidence** | Maps support + grounding + dependence features to a probability via isotonic regression (default) or Platt scaling. |

## What ARGUS-Rerank is not

- **Not a vector retriever.** It re-ranks _your_ retrieval output. Bring your own
  retriever (BM25, dense, hybrid, GraphRAG, HippoRAG, whatever).
- **Not a fact-checker.** It does not adjudicate truth. It quantifies how much
  truly-independent evidence supports a claim.
- **Not a Bayesian inference engine.** The `confidence` score is a calibrated
  empirical estimator, not a posterior. See [`docs/codex/02_v12_canonical_definitions.md`](docs/codex/02_v12_canonical_definitions.md)
  for the precise statement-class taxonomy.
- **Not the full ARGUS system.** This repo is Wedge 1 only. The full reference
  architecture is described in `docs/codex/01_architecture.md` and is a
  separate, larger project.

## Status

Alpha. The API is unstable until 0.2. We follow semver from 0.1 onward; expect
breaking changes on minor bumps until 1.0.

The math layer (`C_eff` weights, saturation parameters) currently uses the
recommended forms from ARGUS Codex §4 D-NEW-1. These will be locked down before
1.0.

## Integrations

- **MCP server**: `argus_rerank.mcp` (stdio + Streamable HTTP). Install with `pip install argus-rerank[mcp]`.
- **LangChain**: see [`langchain-argus-rerank`](https://github.com/VerbalChainsaw/langchain-argus-rerank) (planned).
- **LlamaIndex**: see [`llama-index-postprocessor-argus-rerank`](https://github.com/VerbalChainsaw/llama-index-postprocessor-argus-rerank) (planned).

## Development

### Cursor / VS Code (recommended)

If you use the **ARGUS-Research** monorepo (Codex, PDFs, and this package in one tree), open **`ARGUS.code-workspace` in the repository root** — the folder that contains **`argus/`** and **`ARGUS_CODEX.md`**, not the `argus` subfolder alone.

Then run **`argus-rerank: setup (venv + install)`** from **Run Task** (or `argus/scripts/dev_setup.ps1` / `argus/scripts/dev_setup.sh` from the `argus/` directory). Pick the interpreter under **`argus/.venv/`**. Full checklist: [docs/WORKSPACE.md](docs/WORKSPACE.md).

### Manual setup

```bash
git clone https://github.com/VerbalChainsaw/argus-rerank.git
cd argus-rerank
python -m venv .venv
.venv\Scripts\activate           # Windows
# source .venv/bin/activate      # macOS/Linux
pip install -e ".[dev]"
pytest
```

Linters:

```bash
ruff check .
mypy src/argus_rerank
```

## Contributing

Contributions are welcome under the [Developer Certificate of Origin](https://developercertificate.org/).
Sign every commit with `git commit -s`. See [CONTRIBUTING.md](CONTRIBUTING.md).

We do **not** require a CLA. The license is Apache 2.0 and that's it.

## Citing

If you use **ARGUS-Rerank** in research, please cite the workshop paper (forthcoming):

```bibtex
@misc{argus_rerank2026,
  title  = {Dependence-Aware Reranking: Modeling Source Copying for LLM Retrieval},
  author = {The ARGUS Authors},
  year   = {2026},
  note   = {Software: \url{https://github.com/VerbalChainsaw/argus-rerank}},
}
```

The intellectual lineage is documented in [`NOTICE`](NOTICE) and
[`docs/codex/06_citations.md`](docs/codex/06_citations.md).

## License

[Apache License 2.0](LICENSE).
