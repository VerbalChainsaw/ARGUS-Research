
## 9. Paper templates — three documents, three audiences

### 9.1 Paper 1 — Workshop paper template (the wedge paper)

**Target venues (in priority order):**
1. **UncertaiNLP** at EMNLP 2026 (best topical match — Bayesian fusion, calibration)
2. **FEVER** at ACL/EMNLP recurring (truth-oriented retrieval, single best topical match)
3. **R³AG** at SIGIR-AP recurring (conflict-aware RAG)
4. **GenAI in Finance** at NeurIPS 2026 (domain alignment via KKR/Global Atlantic)

**Length:** 8 pages + references + appendix (typical workshop limits)

**Title candidates:**
- "Dependence-Aware Reranking: Modeling Source Copying for LLM Retrieval"
- "Effective Corroboration: Anti-Double-Counting for Retrieval-Augmented Generation"
- "Beyond Vote Counting: Source-Dependence-Aware Confidence in RAG"

**Section skeleton (carry forward verbatim into actual paper):**

#### 1. Introduction (1 page)
- Open with the FTX or citation-laundering anecdote: 47 documents, 3 truly independent sources, naive RAG gives 47× confidence
- The gap: every published RAG framework treats retrieved passages as conditionally independent
- The contribution: a single named primitive (dependence-aware corroboration) instantiated as a pluggable reranker
- Roadmap

#### 2. Related work (1 page) — REQUIRED CITATIONS
- Self-consistency lineage: Wang 2022, Universal SC, DiVeRSe, Soft SC (§7.1)
- Truth discovery: Yin 2008, Dong 2009, Pochampally 2014 (§7.2) — **single most important comparison**
- Forensic Bayesian networks: Schum 1994, Fenton-Neil-Lagnado 2013 (§7.3)
- Conflict-aware RAG: Wang 2025 RAMDocs, Astute RAG, ECON (§7.7)
- DeepDive/Fonduer as closest system: Niu 2012, Shin 2015, Wu 2018 (§7.10) — **two-paragraph comparison required (D-2026-04)**

#### 3. Method (2 pages)
- Setup: query q, neighborhood N, candidate claims C
- Claim Support Field S(c|q,N) per §3.1
- Effective corroboration C_eff per §3.6 with the typed-edge taxonomy
- Calibration via isotonic regression on per-query-class validation
- **Lock the math layer per D-2026-07** before drafting this section

#### 4. Experiments (2-3 pages)
- Datasets: Stock (Li 2012), RAMDocs (Wang 2025), FEVEROUS (Aly 2021)
- Baselines: vanilla RAG, Self-RAG, FLARE, DeepDive (on Stock)
- Three required ablations per D-2026-05
- Metrics table:

| System | Stock MAE ↓ | RAMDocs EM ↑ | FEVEROUS LA ↑ | ECE ↓ | RC-AUC ↑ |
|---|---|---|---|---|---|
| Vanilla RAG | — | — | — | — | — |
| Self-RAG | — | — | — | — | — |
| FLARE | — | — | — | — | — |
| DeepDive (Stock only) | — | — | — | — | — |
| **PRC + ARGUS (full)** | — | — | — | — | — |
| − dependence penalty | — | — | — | — | — |
| − calibration | — | — | — | — | — |

- Error analysis: when does dependence-aware reranking fail?

#### 5. Discussion (1 page)
- Limitations: model-correlation uncertainty estimation remains hard (D-009 / U_model)
- Falsifiability statement (W-3): "If on a held-out evaluation, removing the dependence penalty does not statistically degrade Stock MAE or RAMDocs EM, the central claim is refuted."
- Connection to truth-discovery lineage; explicit acknowledgment that dependence-handling-for-RAG is the operational contribution

#### 6. Conclusion (0.5 page)

#### Appendix A. ARGUS architecture overview (1 page)
- Brief: how this wedge fits into the full architecture (forward-pointer to Paper 2)
- Pull from Codex §2

#### Appendix B. Implementation details (0.5-1 page)
- Pull from Codex §8.1

#### Appendix C. Statement-class taxonomy (0.5 page)
- Pull from Codex §3.10
- "Theorem hygiene" in the responsible style — see D-2026-06

#### Appendix D. Responsible AI considerations (1-2 pages, **REQUIRED for ML/NLP venues**)
- Surveillance / due process / contestability
- Per Lane 4 ethics-section content: Bender, Birhane, Selbst, Ajunwa, Green
- EU AI Act mapping if applicable
- LLM-as-judge vulnerability discussion (Maloyan 2025)

**Estimated effort:** 4 weeks of writing + 8-12 weeks of experiments. Total 3-4 months from clean draft start.

