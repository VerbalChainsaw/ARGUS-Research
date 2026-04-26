
## 5. Audit history — preserved for provenance

### 5.1 V11 brutal scientific audit (research agent, original)

**Date:** April 25, 2026
**Source:** Research agent extended-search task wf-39b5c498
**Verdict tags used:** ESTABLISHED / NOVEL_DEFENSIBLE / NOVEL_QUESTIONABLE / MISAPPROPRIATED / RESTATEMENT

**Citation verification (all six pass):**
- Wang 2022 self-consistency (arXiv 2203.11171) — EXISTS_AS_CITED
- Xie 2024 calibrating reasoning (arXiv 2405.18711) — EXISTS_AS_CITED
- Knappe 2024 semantic SC (arXiv 2410.07839) — EXISTS_AS_CITED
- Hwang 2024 source reliability RAG (arXiv 2410.22954, EMNLP 2025) — EXISTS_AS_CITED
- Taubenfeld 2025 confidence SC (arXiv 2502.06233, ACL 2025) — EXISTS_AS_CITED
- Wu 2025 temperature TTS (arXiv 2510.02611) — EXISTS_AS_CITED

**Terminology audit verdicts:**
| Term | Verdict |
|---|---|
| Posterior field | NOVEL_QUESTIONABLE leaning MISAPPROPRIATED |
| Principal-chain regression | MISAPPROPRIATED |
| Continuous temperature | NOVEL_DEFENSIBLE |
| Temperature cloud | PURE_METAPHOR |
| Contrail thickness | PURE_METAPHOR |
| Evidence geometry / manifold | NOVEL_QUESTIONABLE |
| Conflict lanes / divergence ridges | PURE_METAPHOR |
| Anchor hubs | NOVEL_DEFENSIBLE |
| Branch corridors | PURE_METAPHOR |
| Chase / chase-driven proof closure | MISAPPROPRIATED (high confidence) |

**Architectural prior-art verdicts:**
| Claim | Verdict |
|---|---|
| Filesystem-as-epistemic-control | RESTATEMENT (medallion architecture, DIKW) |
| Six-stratum epistemic separation | RESTATEMENT (DIKW, F3EAD, OAIS, KG pipelines) |
| Multi-regime sampling for posterior | RESTATEMENT (DiVeRSe, Universal SC, Boosted Prompts) |
| Evidence dependence law | INCREMENTAL leaning RESTATEMENT (Schum 1994, Dong 2009) |
| Six-component uncertainty | INCREMENTAL (Hou 2024, Taparia 2025, TRAQ 2024) |
| Provenance vs authenticity | RESTATEMENT (W3C PROV, Cheney 2009, C2PA) |
| Calibrated decision probabilities | RESTATEMENT in active area (Guo 2017, Kadavath 2022) |
| Active retrieval as EIG | INCREMENTAL — most defensible novel direction |

**Math rigor findings:**
- d_A fails as metric (D-003)
- "Tensor" misuse (D-002)
- "Regression" misuse (D-004)
- Continuous-T derivatives need finite differences with score-function or pathwise alternatives (D-005)

**Theorem hygiene verdict:** §26 reclassification is "genuine and unusual rigor" — rare in LLM-systems specs, materially raises credibility. Lipton & Steinhardt 2018 "Troubling Trends in ML Scholarship" called for exactly this.

**Integrated novelty verdict:** Defensible only as engineering integration. **DeepDive/Fonduer is the unavoidable comparison system covering 3 of 4 PRC pillars.**

**Strongest defensible novel direction:** Active retrieval as Lindley EIG estimator computable from multi-regime samples PRC already has.

**Key citation gaps identified:** Schum 1994; Bovens & Hartmann 2003; Yin/Han/Yu 2008 (TKDE); Dong/Berti-Equille/Srivastava 2009 (PVLDB); Pochampally 2014 (SIGMOD); Fenton & Neil 2018; Guo 2017 (ICML); Kadavath 2022; Tian 2023 (EMNLP); Lin 2022 (TMLR); Wang 2022 + variants (Universal SC, Adaptive Consistency, DiVeRSe, Soft SC, Boosted Prompts, Batched SC); Maier/Mendelzon/Sagiv 1979 chase; Fagin/Kolaitis/Miller/Popa 2005; Cheney/Chiticariu/Tan 2009; Green/Karvounarakis/Tannen 2007 provenance semirings; W3C PROV-DM 2013; Lindley 1956; MacKay 1992; Houlsby BALD 2011; Foster ICML 2021; FLARE (Jiang EMNLP 2023); Self-RAG (Asai ICLR 2024); Atlas (Izacard JMLR 2023); REPLUG; CRAG; Angelopoulos & Bates 2023; Mohri & Hashimoto 2024; Quach 2024; Cherian 2024; Vovk 2022.

### 5.2 Lane 1 — Verification audit (V12 vs V11 audit)

**Date:** During this conversation
**Method:** Internal cross-reference of every V11 audit defect against V12 response

**Headline result:** V12 cleanly fixed 8 of 14 defects, partially fixed 4, left 2 as promise-without-delivery, and introduced 5 new defects of its own.

**Cleanly fixed:** D-001 (renamed Posterior→Support), D-002 (renamed Tensor→Function), D-003 (downgraded Metric→Dissimilarity), D-004 (renamed Regression→Selection), D-006 (Bayesian framing repaired), D-012 (formal-core scrubbed of "posterior"), D-research-1 (renamed Chase→Pursuit), D-005 (finite-difference doctrine added).

**Partially fixed:** D-007 (utility components partly typed), D-009 (U_model named but not estimated), D-011 (per-query-class calibration mentioned), D-research-4 (EIG named as target but no estimator).

**Promise without delivery:** D-research-2 (citation list), D-research-3 (DeepDive comparison).

**Unaddressed:** D-008 (KDE connection), D-010 (Lanes undefined).

**New defects:** D-NEW-1 through D-NEW-5 — see §4.3 above.

### 5.3 Lane 2 — Reviewer simulation

**Date:** During this conversation
**Method:** Hostile-reviewer mode across three profiles: PODS/SIGMOD theory, EMNLP/NAACL/TACL, TKDE/VLDB systems

**Reviewer A (PODS/SIGMOD theory) verdict:** Reject. Resubmit with semiring-based provenance and termination/complexity analysis of pursuit loop.

**Reviewer B (EMNLP/NAACL/TACL) verdict:** Reject. No experiments. Self-consistency literature underspoken. Architecture unfalsifiable as written. Calibration claims aspirational.

**Reviewer C (TKDE/VLDB systems) verdict:** Major revision. DeepDive treatment one-sentence — must be dedicated section. Truth-discovery dependence handling needs Dong 2009 / Pochampally 2014 comparison. Real benchmark required.

**Three killing blows that all reviewers hit:**
1. No experiments → reject everywhere except arXiv-only / vision-paper venues
2. DeepDive/truth-discovery treatment one-sentence → reject from any KBC/IR venue
3. No falsifiability statement → suspicion of unfalsifiability from any rigorous reviewer

**All three are fixable with editorial work, not architecture changes.** No reviewer would say "your architecture is wrong." They'd say "your paper is wrong."

### 5.4 Lane 3 — Implementation gap analysis

**Date:** During this conversation
**Method:** Walk through V12 in build order, classify each component as BUILDABLE / NEEDS_SPEC / NEEDS_RESEARCH / NEEDS_PROTOTYPE_FIRST

**Headline result:** ~60% of V12 is buildable from the document alone. The 40% that isn't is concentrated in the math layer (§4) and dependence layer (§10) — exactly where the architecture's claimed contribution lives.

**Critical-path build sequence (for a competent senior engineer):**

| Sprint | Deliverable | Status |
|---|---|---|
| 1-2 | Filesystem strata + object schemas | BUILDABLE |
| 3-4 | Provenance/lineage with PROV-DM | NEEDS_SPEC |
| 5-8 | Normalization extractor v0 (LLM-based) | NEEDS_RESEARCH (research-prototyping) |
| 9-10 | Regime sampling harness | BUILDABLE |
| 11-12 | CSF estimator + grounding score | NEEDS_SPEC |
| 13-16 | Dependence DAG + δ function | HARDEST UNSOLVED PIECE |
| 17-18 | Uncertainty profile | PARTIAL — U_norm/U_model under-specified |
| 19-20 | Closure policy + admissibility | NEEDS §8 reformulation |
| 21-24 | Evidence pursuit loop | NEEDS H specification |
| 25+ | Calibration on validation data | NEEDS_PROTOTYPE_FIRST |

**Realistic prototype timeline:** 6 months for solo engineer, 3 months for team of three, *if* V13 closes the math layer first. Otherwise engineers will reinvent specifics and produce divergent implementations.

**Three unbuildable sentences:** §4.3, §4.6, §8 — see D-NEW-1 and D-NEW-3.

### 5.5 Lane 4 — Publication readiness research

**Date:** During this conversation
**Source:** Research agent extended-search task wf-acdbc1ee
**Method:** Realistic venue analysis given V12's narrowed claim and zero empirics

**Headline finding:** V12 in current form is **not publishable at any peer-reviewed venue with a meaningful empirical bar**. arXiv is the only no-friction option. Realistic peer-reviewed homes are workshops with minimal experiments (3-4 months), CIDR 2027 if substantially rewritten with academic co-author (5-7 months, 10-30% odds), or MLSys 2026 Industrial Track with deployed benchmarks (4-6 months, 30-45% odds).

**Critical canonization data:**
- Not one comparable systems paper (DeepDive, Fonduer, Self-RAG, GraphRAG, HippoRAG, FLARE, Atlas) contains formal theorems in main text. Theory inflation does not earn credit.
- Recommended primary template: **Shin et al. 2015 DeepDive Incremental** (PVLDB 8(11)) — closest structural model, 12 pages, 50/50 architecture/experiments split, two narrowed contributions.
- Recommended secondary template: **HippoRAG (Gutiérrez 2024 NeurIPS)** — single-mechanism story with diagnostic appendix.
- Templates to avoid: Atlas (43 pages), Self-RAG (requires training critic+generator), GraphRAG (depends on open-source release at scale).

**Required experimental minimum (three ablations, three datasets):**
1. PRC vs vanilla RAG baseline (non-negotiable)
2. Ablate dependence penalty (non-negotiable for the headline claim)
3. Ablate calibration layer (non-negotiable for uncertainty-decomposition claim)

**Recommended datasets:**
- **Stock** (Li et al. 2012 VLDB, ~16K stock items × 55 sources) — canonical truth-discovery benchmark where source copying dominates
- **RAMDocs** (Wang et al. 2025 arXiv 2504.13079) — most current conflict-aware RAG benchmark; LLama3.3-70B reaches 32.6 EM
- **FEVEROUS** (Aly et al. NeurIPS 2021) — 87K claims with sentence- and table-cell evidence

**Optional fourth dataset:** **Population-City-Year** (Pasternack & Roth 2010 COLING) for numerical truth discovery.

**DeepDive maintenance status (verified April 2026):** DEAD. Last release 2017–2021. Toolchain rot prevents revival. No actively-maintained successor in the lineage. **Niche is unoccupied.**

**Key venue-specific data:**
- CIDR 2026 already past deadline; CIDR 2027 CFP expected Sept/Oct 2026; 6 pages including refs
- MLSys 2026 Industrial Track: novelty NOT required; design methodology + benchmarks; anonymized authors but company names allowed; **highest-credential venue with lowest novelty bar for this engineer's profile**
- CACM Practice section (under EiC Terence Kelly, recently rebooted): unsolicited submissions accepted, ≤6,000 words, code encouraged, criteria practicality+rigor. Pitch EiC by email first.
- IEEE Intelligent Systems Trends and Controversies department: practitioner-friendly, 10-20% odds without empirics.

**The recommended sequenced path (6-month plan):**
1. Month 1: arXiv preprint of V12-equivalent. Engage legal/comms on sanitized framing.
2. Months 1-3: Build three required ablations on Stock + RAMDocs + FEVEROUS. Add DeepDive baseline on Stock.
3. Month 4: Write 8-page workshop paper for UncertaiNLP / FEVER / R³AG.
4. Month 5: Pitch CACM Practice article to Terence Kelly. Submit QCon AI talk.
5. Month 6+: Expand to full venue submission. Engage academic collaborator for FAccT workshop ethics paper.

### 5.6 Canonization research (final research lane)

**Date:** During this conversation
**Source:** Research agent extended-search task wf-de60365d
**Target:** Working system that gets seen and demoed (#3) with reference architecture as second-order leverage (#2)

**Five-element canonization stack (must hit all five):**
1. Named primitive in one phrase
2. Pip-installable artifact runnable in <1 hour
3. Same-day multi-channel launch (paper + repo + blog + social)
4. Specific killer-demo domain
5. Institutional credibility signal

**The Hazy Research recipe to imitate:**
- Single named owner inside recognized lab umbrella
- Primitive expressible as kernel or decorator
- Paper + plain-English blog post
- Versioned series cadence (FA→FA2→FA3; S4→Mamba→Mamba-2)
- Commercial monetization off to the side via spinoff (Snorkel Flow), OSS stays free

**Demo domain ranking (top picks):**
1. **FTX/Theranos court records** (CourtListener) — marketing demo, post-conviction so zero defamation risk, vivid and tweetable
2. **Citation laundering** (OpenAlex CC0 + Retraction Watch + S2ORC) — primary technical artifact, citations literally are dependence DAG, scite.ai is closest competitor and doesn't do dependence-correction
3. **Enron claims-and-contradictions** (CMU/EDRM corpus, EnronQA Aug 2025) — reproducible benchmark, RAG-over-comms canonical

**Strategic windows:**
- **OCCRP/Aleph open-source sunset Dec 31, 2025** — opens investigative-tooling vacuum. NICAR 2027 (March 2027) and IRE 2027 land in this window.
- **MCP at 97M monthly SDK downloads (Dec 2025)** — donated to Linux Foundation Agentic AI Foundation. Distribution surface incumbents haven't occupied.
- **2022-2024 SEC/CFTC enforcement wave: $3.5B+ in fines** for off-channel comms. Smarsh / Behavox / Theta Lake all ship explainability but not source-dependence detection. ARGUS positioned as pre-competitive open standard ("the NIST of propagation-aware comms surveillance") = right monetization target 12-24 months out.

**The wedge to ship first:** **ARGUS-Rerank** (`argus-rerank` on PyPI, import `argus_rerank`). ~500 lines of Python. Standalone PyPI library + MCP server (`argus_rerank.mcp`) + LangChain partner package + LlamaIndex integration.

**License:** Apache 2.0 + DCO-only contributions. (Every BSL/SSPL/FSL relicense in last 3 years produced community fork: OpenSearch, OpenTofu, Valkey.)

**Documentation:** MkDocs Material or Mintlify. Three pillars: concepts / how-to cookbook / API reference. 3-5 launch notebooks all Colab-runnable in <5 min. Publish `llms.txt` at root.

**Community:** Defer Discord. GitHub Issues + Discussions only for first 3 months. Solo maintainer at financial firm with full-time job will burn out moderating.

**Twitter is not optional:** ~1-2 substantive threads/week for 12 months minimum. Without this the wedge ships into silence.

**18-month canonization probability conditional on disciplined execution:** 15-25% (high relative to baseline rate for new RAG projects, well under 5%).

