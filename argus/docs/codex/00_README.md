
## 1. README — Why this Codex exists

### 1.1 The problem this document solves

Between April 2026 and now, the PRC + ARGUS architecture has gone through four overlapping streams of work:

1. **V11 specification** — 51-page integrated architecture (Probabilistic Reasoning Cartography + ARGUS unified spec)
2. **V11 brutal scientific audit** — terminology audit, prior-art check, defect list across math, novelty, and literature
3. **V12 corrective redraft** — additive corrective pass that absorbed the audit's recommendations
4. **V12 four-lane evaluation** — verification audit, hostile reviewer simulation, implementation gap analysis, publication-readiness research

The cumulative output is roughly **80,000 words of analysis, audits, and revisions** spread across multiple PDFs, evaluation files, and research-agent reports. Without consolidation, that work fragments — pieces of insight lost in conversation history, defects re-discovered, decisions silently overturned.

This Codex unifies all of it into a single source-of-truth from which every future artifact (paper, wedge, blog post, talk, codebase) can be carved.

### 1.2 What survived

Despite the demolition feel of four evaluation passes, **the architecture is mostly intact**. What got destroyed was the framing, not the substance. Specifically:

**Survived intact:**
- The integration thesis (filesystem strata + dependence-aware corroboration + multi-regime sampling + calibrated closure)
- §13 evidence dependence law as the strongest defensible kernel
- Theorem hygiene (§19/§26) as a credibility move
- The §22 ordered pipeline as a usable engineering blueprint
- Active retrieval as Lindley EIG — the highest-leverage technical opportunity
- ARGUS dissimilarity (post-rename) as a routing primitive
- The six-component uncertainty profile (§7)
- Multi-modal evidence contracts (§14)
- Budget modes (§18)

**Renamed but preserved:**
- Claim Posterior Field → Claim Support Field
- Principal-chain regression → Principal-chain selection
- Chase-driven proof closure → Evidence pursuit loop
- Spread-control tensor → Spread-control function
- Metric d_A → ARGUS dissimilarity d_A

**Promoted to headline:**
- Dependence-aware corroboration (was §13, now the wedge contribution)
- Calibrated closure (was support layer, now standalone subproblem)

**Deprecated:**
- Posterior field semantics (without explicit prior + likelihood)
- Temperature cloud / contrail thickness / divergence ridges / branch corridors as formal terms
- Theoretical-novelty claims for individual primitives

### 1.3 What this Codex is *not*

This is not a finished paper. It is the source library from which papers are written. Trying to read it as a paper will produce frustration; reading it as a library produces clarity.

### 1.4 The forward path in one paragraph

The strongest publication path is **wedge-first**: ship dependence-aware reranking as a standalone PyPI package + MCP server, prove it on Enron + citation-laundering benchmarks, write a workshop paper around it (UncertaiNLP / FEVER / R³AG), and let the full ARGUS reference architecture follow as a 12-month follow-on. The integrated-system paper becomes the *second* paper, citing the wedge as established work. Section 9 contains the templates for both.

