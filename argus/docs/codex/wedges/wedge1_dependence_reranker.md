
## 8. Wedge templates — what to build first

### 8.1 Wedge 1 — Dependence-aware reranker

**Status:** PRIMARY WEDGE. This is the first artifact to ship.

**One-line definition:** A standalone Python library that, given a query and a set of retrieved documents, computes per-document dependence weights and produces a re-ranked list with calibrated confidence on the underlying claim.

**Naming** (check PyPI and GitHub before publishing):
- **Chosen:** **ARGUS-Rerank** — product name; PyPI / CLI `argus-rerank`; import package `argus_rerank`.
- **Alternates if PyPI collision:** `argus-dependence-rerank`, `provrank`.
- `evidently-rerank` — REJECTED (collides with existing observability tool).

**Target installation experience:**
```bash
pip install argus-rerank
```

```python
from argus_rerank import DependenceAwareReranker

reranker = DependenceAwareReranker()
results = reranker.rerank(
    query="Were FTX customer funds segregated from Alameda?",
    documents=retrieved_docs,
    return_dependence_graph=True
)

print(f"Effective independent sources: {results.effective_n}")
print(f"Calibrated confidence: {results.confidence:.2f}")
```

**Core technical components (~500 lines):**
1. **Near-duplicate detection** (~80 lines): SimHash + MinHash, configurable threshold
2. **Citation-graph collapse** (~100 lines): typed edges from §3.6 dependence taxonomy
3. **Copy-language detection** (~80 lines): n-gram overlap + LLM-based copy attribution as fallback
4. **Effective corroboration C_eff computation** (~100 lines): per §3.6, with saturation (logarithmic damping recommended)
5. **Calibrated confidence layer** (~80 lines): isotonic regression default, Platt scaling fallback
6. **Result API + types** (~60 lines): clean Pydantic models

**Surface area:**
- Standalone Python library (the core)
- MCP server (`argus_rerank.mcp`) — both stdio and Streamable HTTP
- LangChain partner package: `langchain-argus-rerank` implementing `BaseDocumentCompressor`
- LlamaIndex integration: `llama-index-postprocessor-argus-rerank`

**Required benchmarks for credibility:**
- **Stock dataset** (Li et al. 2012 VLDB): "Recovers ground-truth source count to within 10%; reduces effective citation count by 73% on controlled subset."
- **RAMDocs** (Wang et al. 2025): "+11.4 EM points over vanilla RAG on conflicting evidence subset."
- **Enron California-energy-claims subset**: reproducible benchmark released as part of this repo.

**Documentation pages required at launch:**
1. README with 30-second quickstart
2. Concept page: "What is dependence-aware corroboration?"
3. Five Colab notebooks (quickstart, Enron, citation laundering, MCP, LangChain)
4. API reference auto-generated via mkdocstrings
5. `llms.txt` at root

**Launch checklist (same day):**
- [ ] GitHub repo public with README, LICENSE (Apache 2.0), CONTRIBUTING (DCO), code, tests, notebooks
- [ ] PyPI package published (`pip install argus-rerank` works)
- [ ] arXiv preprint submitted (reserve number ahead of time)
- [ ] Technical blog post published (3,000 words)
- [ ] Twitter/X thread (10-12 posts)
- [ ] HN "Show HN" submitted (Tuesday or Wednesday morning, US timezone)
- [ ] Reddit posts (r/MachineLearning, r/LocalLLaMA, r/LangChain)
- [ ] MCP Registry submission
- [ ] PulseMCP submission
- [ ] DM to 5 YouTube tutorial creators with Colab link
- [ ] LangChain partner-package PR opened within 7 days

**First-30-days targets:**
- 500 GitHub stars
- 1,000 PyPI downloads
- 1 tutorial video by an external creator

**Failure modes to monitor:**
- Scope creep into full ARGUS during build (FATAL — see Codex §6 D-2026-01)
- Publishing into silence without Twitter presence
- Broken installation on reviewer machines (run reproducibility test on three platforms before launch)
- Unfair benchmark setup that gets flamed (have a third party verify the Stock + RAMDocs numbers before publishing)

