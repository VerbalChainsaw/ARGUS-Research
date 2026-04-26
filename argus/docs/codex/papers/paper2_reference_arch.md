
### 9.2 Paper 2 — Reference architecture template

**Target venues (in priority order):**
1. **CIDR 2027** (6 pages including references; vision-paper friendly; requires academic co-author for solo industry submission)
2. **MLSys 2026 Industrial Track** (no novelty required; deployment metrics are gating; anonymized authors but company names allowed)
3. **arXiv preprint as canonical citation** (no peer review; companion to a CACM Practice piece)
4. **EMNLP / ACL / KDD main track** as resubmission target after workshop paper (Paper 1) is accepted

**Length:** 12-25 pages depending on venue

**Title candidates:**
- "ARGUS: A Reference Architecture for Truth-Oriented Retrieval and Reasoning"
- "PRC + ARGUS: Dependence-Aware, Calibration-Tested Forensic-Grade Document Understanding"
- "Stratified Evidence: An Engineering Architecture for High-Stakes RAG"

**Section skeleton:**

#### 1. Introduction (1.5 pages)
- The problem: high-stakes document analysis where RAG hallucinations and corroboration inflation matter
- The gap: no published RAG framework integrates stratification + dependence + multi-regime sampling + calibration
- The contribution: integrated reference architecture, narrowed novelty per D-2026-09
- Roadmap

#### 2. Related systems and prior art (2 pages)
- DeepDive/Fonduer detailed comparison — see D-2026-04 (full two-page comparison subsection)
- GraphRAG, HippoRAG, Self-RAG, FLARE positioning
- Truth discovery lineage and why it has not been applied to RAG
- Forensic Bayesian networks as engineering precedent

#### 3. ARGUS architecture (3-4 pages)
- Pull verbatim from Codex §2
- Six storage strata
- Operational pipeline
- The five primitives table

#### 4. Formal definitions (2-3 pages)
- Pull from Codex §3 (V12 canonical definitions)
- Statement-class taxonomy (§3.10)
- The math layer with locked-down forms per D-2026-07

#### 5. Implementation (2-3 pages)
- Pull from Codex §5.4 (Lane 3 implementation gap analysis) reorganized as a build-order narrative
- Code excerpts from the wedge (§8.1) showing the dependence-aware-reranker as concrete instance
- Multi-modal contracts (V12 §14)
- Budget modes (V12 §18)

#### 6. Evaluation (2-3 pages)
- Same three required ablations as Paper 1, possibly expanded to additional datasets
- Comparison table extended with DeepDive baseline on additional benchmarks
- Case studies: Enron + citation laundering as worked examples

#### 7. Limitations and future work (1 page)
- Open problems explicitly named:
  - Model-correlation uncertainty estimation (D-009)
  - Dependence-edge inference at scale
  - Calibration under distribution shift
  - Prompt injection resistance for evidence corpora
- Each tagged with whether it's a research direction or an engineering improvement

#### 8. Responsible AI (1-2 pages)
- Same scaffolding as Paper 1 §D
- Expanded to address forensic-workplace-evidence framing if venue permits
- Per Lane 4 ethics content

#### 9. Conclusion (0.5 page)

#### Appendix: Defect register
- Pull selected entries from Codex §4 — the public-facing defects (D-008, D-009, D-NEW-1) demonstrate ongoing rigor

**Estimated effort:** 6-8 weeks of writing assuming experiments from Paper 1 are available. 5-7 months total if starting from V12 baseline.

