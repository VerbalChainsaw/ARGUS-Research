# ARGUS Codex
### Unified working document for the PRC + ARGUS architecture
### Director Gabriel Steenhoek | KKR / Global Atlantic
### Version 1.0 — consolidated from V11 + V12 + four evaluation lanes

---

## Manifest

This is a single-file delivery of what should logically be a multi-file repository. Each section below carries an HTML-comment file marker (`&lt;!-- FILE: path --&gt;` ... `&lt;!-- END FILE --&gt;`) so the document can be mechanically split into the target directory structure later. A split script is included at the bottom.

Target repository structure when split:

```
codex/
├── 00_README.md                      ← Section 1
├── 01_architecture.md                ← Section 2
├── 02_v12_canonical_definitions.md   ← Section 3
├── 03_defects.md                     ← Section 4
├── 04_audits/
│   ├── v11_audit.md                  ← Section 5.1
│   ├── lane1_verification.md         ← Section 5.2
│   ├── lane2_reviewer_sim.md         ← Section 5.3
│   ├── lane3_implementation_gaps.md  ← Section 5.4
│   └── lane4_publication_strategy.md ← Section 5.5
├── 05_decisions.md                   ← Section 6
├── 06_citations.md                   ← Section 7
├── wedges/
│   ├── wedge1_dependence_reranker.md ← Section 8.1
│   ├── wedge2_provenance_loader.md   ← Section 8.2
│   └── wedge3_calibration_layer.md   ← Section 8.3
├── papers/
│   ├── paper1_workshop_template.md   ← Section 9.1
│   ├── paper2_reference_arch.md      ← Section 9.2
│   └── paper3_practitioner_essay.md  ← Section 9.3
└── 99_split_script.sh                ← Section 10
```

**How to use this document:**

- **First pass on phone:** read top to bottom. The narrative is structured to make sense end-to-end. Sections 1–4 give you state-of-the-architecture. Section 5 is the audit history. Section 6 is the decision log. Sections 8–9 are the carry-forward templates for actual writing.
- **Second pass on desktop:** run the split script in Section 10 to produce the directory structure, then push to GitHub.
- **For any future wedge:** start from the matching template in Section 8 or 9, pull supporting material from earlier sections by reference.

Status legend used throughout:

| Tag | Meaning |
|---|---|
| **INTACT** | Survived all audit lanes, use as-is |
| **RENAMED** | Concept survived, name changed in V12 |
| **PARTIAL** | Addressed but residual defect remains |
| **UNADDRESSED** | Original defect still open |
| **NEW** | Defect introduced by V12 itself |
| **PROMOTED** | Subsidiary idea elevated to headline contribution |
| **DEPRECATED** | Removed from formal core, kept only for historical comparison |

---

<!-- FILE: codex/00_README.md -->

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

<!-- END FILE -->

---

<!-- FILE: codex/01_architecture.md -->

## 2. Architecture — what ARGUS actually is

### 2.1 One-paragraph definition

**ARGUS is a forensic-grade evidence-management filesystem and reasoning architecture for high-stakes organizational document analysis.** It ingests organizational exhaust (email, ticket systems, chat, meeting transcripts, attached documents) into stratified storage, normalizes content into typed claims with explicit provenance, models source dependence to prevent corroboration inflation, samples reasoning across multiple regimes to estimate claim support, applies typed uncertainty decomposition, and emits closure decisions tied to query-class-specific calibration. It is positioned as the integrity layer beneath enterprise RAG, not a replacement for it.

### 2.2 The six layers, top down

1. **Decision layer** — query class admissibility, closure policy, action selection (Close / Provisional / Contest / Abstain / Pursue / Escalate)
2. **Calibration layer** — maps support + grounding + dependence + uncertainty features to calibrated decision probabilities (Brier, ECE, reliability diagrams, conformal where applicable)
3. **Reasoning layer** — claim support estimation under multi-regime LLM sampling, principal-chain selection, evidence pursuit loop
4. **Evidence layer** — claim atomization, entity binding, temporal qualification, dependence DAG construction, conflict surfacing
5. **Normalization layer** — phi(r) operator, claim canonicalization with reversible merge/split, normalization confidence
6. **Storage layer** — ARGUS filesystem strata: 00_raw → 01_normalize → 02_evidence → 03_graph → 04_time → 05_decision → ... → 09_policy

### 2.3 Storage strata (V11 §3 preserved into V12)

```
00_raw/         immutable source material with hash + provenance
01_normalize/   parsed and chunked content, claim atoms
02_evidence/    typed evidence claims with grounding metadata
03_graph/       entity, relation, dependence DAG
04_time/        temporal alignment, bitemporal records
05_decision/    closure outputs, support fields, calibrated probabilities
06_index/       retrieval indexes (vector, BM25, structural)
07_replay/      version bundles, reproducibility traces
08_provenance/  lineage records, version-bundle hashes, replay state
09_policy/      governance objects, admissibility rules, query-class config
```

**Stratification rule (non-negotiable):** content never moves up-stream. A decision object cannot be cited as raw evidence. A normalized claim cannot be re-canonicalized as the source. Stratification gives the system its integrity property.

### 2.4 Operational pipeline (V12 §22, off-by-one numbering corrected)

1. Ingest evidence snapshot, record version bundle
2. Parse query → query class, stakes level, budget mode
3. Build ARGUS-compliant neighborhood: temporal narrowing, entity anchoring, conflict surfacing
4. Normalize evidence into claim atoms with lineage and confidence
5. Construct/update dependence edges for the query neighborhood
6. Sample reasoning trajectories across regime set, project into claim space
7. Estimate Claim Support Field, grounding-adjusted support, regime instability
8. Assemble uncertainty profile by component
9. Run evidence pursuit loop iff closure policy says more evidence could change the decision
10. Recompute support and uncertainty after each substantial neighborhood change
11. Apply query-class admissibility and calibrated closure policy
12. Emit final / provisional / contested / abstained / escalated output with provenance + unresolved-conflict status
13. Record replay metadata and decision trace

### 2.5 The five primitives that carry the architecture

| Primitive | What it does | V12 status |
|---|---|---|
| **Stratified storage** | Prevents cross-contamination between source material, derived analysis, and decisions | INTACT |
| **Claim Support Field S(c\|q,N)** | Trajectory-marginalized support estimator over normalized claims | RENAMED (was Claim Posterior Field) |
| **ARGUS dissimilarity d_A** | Routing-oriented dissimilarity over evidence neighborhoods | RENAMED (was metric d_A) |
| **Dependence DAG with effective corroboration C_eff** | Anti-double-counting of correlated evidence | INTACT but under-specified (see §4 D-NEW-1) |
| **Six-component uncertainty profile U(c)** | Typed uncertainty enabling remedy routing | INTACT |

### 2.6 What ARGUS is *not*

- Not a replacement for vector RAG (it sits beneath or alongside it)
- Not a Bayesian inference engine (no explicit priors or likelihoods unless Gibbs extension is invoked)
- Not a knowledge-base construction system in the DeepDive sense (it is RAG-flavored, not factor-graph-flavored)
- Not a forensic adjudicator (humans adjudicate; ARGUS structures evidence and surfaces uncertainty)

<!-- END FILE -->

---

<!-- FILE: codex/02_v12_canonical_definitions.md -->

## 3. Canonical V12 definitions — the formal core

These are the V12-locked definitions. Every paper, blog post, and code module should use these terms verbatim. Renamed terms have their V11 originals listed for historical reference only.

### 3.1 Claim Support Field

**Definition.** A regime-indexed, query-conditioned, neighborhood-conditioned support estimator over normalized claims. It is an empirical object derived from sampled reasoning trajectories after normalization into claim space. It is *not* a Bayesian posterior by default.

**Formal expression:**
```
S(c | q, N) = (1/Z_S) · Σ_ρ α_ρ · Σ_r w(r,c,q,N,ρ) · 1[c ∈ φ(r)]
```

**V11 name:** Claim Posterior Field (deprecated — see §4 D-001).

**Outstanding spec gap:** Z_S, w(·), and α_ρ are template-level. See §4 D-NEW-1 for the lock-down required before implementation.

### 3.2 Principal-chain selection

**Definition.** The process of selecting one chain, one partial chain, or one canonical synthesis path from a candidate family under an explicit energy or score function. An optimization over candidate chains, not a statistical fit.

**V11 name:** Principal-chain regression (deprecated — see §4 D-004).

### 3.3 Evidence pursuit loop

**Definition.** The iterative retrieval-and-verification process that expands the admissible evidence frontier when uncertainty remains too high for closure. Target objective: expected ambiguity reduction per unit cost.

**V11 name:** Chase / chase-driven proof closure (deprecated — see §4 D-research-1).

### 3.4 Spread-control function

**Definition.** A function (or, when discretized, a table) that maps regime features, evidence features, and query features to an operational dispersion parameter used to tune exploration, abstention tolerance, or retrieval widening. Not a tensor unless a multilinear construction is proven.

**V11 name:** Spread-control tensor (deprecated — see §4 D-002).

### 3.5 ARGUS dissimilarity

**Definition.** A nonnegative routing-oriented dissimilarity defined over evidence objects. Not a metric unless each component is proven metric and the composition preserves metric axioms.

**Formal expression:**
```
d_A(x_i, x_j) = λ_t·d_t + λ_e·d_e + λ_s·d_s + λ_c·d_c + λ_x·d_x
```

where d_t is temporal separation, d_e is entity/canonical-neighborhood separation, d_s is source-type separation, d_c is content dissimilarity, and d_x is contradiction or conflict tension.

**V11 name:** ARGUS metric d_A (deprecated — see §4 D-003).

### 3.6 Effective corroboration C_eff

**Definition.** A dependence-adjusted aggregate of evidence supporting a claim, where typed dependence edges discount naive corroboration counts.

**Formal template (V12 §4.6):**
```
C_eff(c) = Σ_i u_i − Σ_{i<j} δ_ij
```

**Outstanding spec gap:** u_i and δ_ij are template-level. See §4 D-NEW-1.

**Typed dependence edge taxonomy (V12 §10):**
- `derived-from`
- `mirrors`
- `summary-of`
- `quote-of`
- `same-author-same-event`
- `same-thread`
- `same-ticket`
- `same-generated-summary`

### 3.7 Six-component uncertainty profile

**Definition.** A typed uncertainty vector U(c) = (U_retrieval, U_coverage, U_conflict, U_norm, U_reasoning, U_model), where each component is a typed uncertainty source enabling remedy routing.

| Component | Symptom | Remedy |
|---|---|---|
| U_retrieval | Sparse support, strong query relevance | Widen neighborhood |
| U_coverage | Known references to missing items | Complete traversal |
| U_conflict | Sources materially disagree | Surface conflict |
| U_norm | Claim merges or bindings unstable | Re-normalize |
| U_reasoning | Support swings across regimes | Delay closure |
| U_model | High consensus, low evidence fit | Verifier or abstain |

### 3.8 Action set and closure decision

**Action set:** A = {CloseFinal, CloseProvisional, EmitContested, Abstain, PursueMoreEvidence, EscalateHuman}

**Closure objective (V12 §8):**
```
a* = argmin_a E[L(a, θ; k) | observed evidence, support profile, uncertainty profile]
```

where k is query class and θ is the latent evidentiary state.

**Outstanding spec gap:** E[·|·] over θ is uncomputable as written. See §4 D-NEW-3 for the reformulation around expected loss under the support distribution.

### 3.9 Calibration law

**Definition (V12 §11).** A calibration layer maps feature vectors derived from support, grounding, dependence, uncertainty, provenance, and coverage into estimated decision probabilities or confidence scores. Estimation and calibration are explicitly separate.

**Required evaluation:** Brier score, ECE, reliability diagrams, selective risk under abstention. **Per query class, not generic.**

### 3.10 Statement-class taxonomy

Every mathematically-flavored statement must be labeled as one of:

| Class | Required content |
|---|---|
| Definition | Precise definitions and direct derivation |
| Architecture-conditional proposition | Explicit assumptions and failure cases |
| Heuristic / objective template | Why reasonable; no proof language |
| Empirical hypothesis | Falsification condition and evaluation plan |
| Engineering rule | Operational rationale |
| Conjecture / future work | Reason for plausibility |

The word **theorem** is reserved for statements with actual proof under stated assumptions. There are currently no theorems in ARGUS.

<!-- END FILE -->

---

<!-- FILE: codex/03_defects.md -->

## 4. Defect register — the live status board

### 4.1 V11-originated defects (status post-V12)

#### D-001 — "Posterior" without Bayesian structure
**Status:** RESOLVED in formal core; **PARTIAL** in colloquial use
**Original severity:** MAJOR → **MINOR after V12 §11**
**Resolution:** V12 renamed to Claim Support Field. Gibbs-posterior extension confined to optional appendix.
**Residual:** Some V12 sections still use "posterior" colloquially. Scrub before publication.

#### D-002 — "Tensor" misuse for Σ_spread
**Status:** RESOLVED
**Severity:** MAJOR → **N/A**
**Resolution:** V12 §3.6 renamed to spread-control function.

#### D-003 — d_A asserted metric without proof
**Status:** RESOLVED — exemplary fix
**Severity:** MAJOR → **N/A**
**Resolution:** V12 §5.1 explicitly downgrades to ARGUS dissimilarity. §5.2 documents which components may/may not be metric. d_x (contradiction tension) explicitly flagged as non-metric.

#### D-004 — "Principal-chain regression" not regression
**Status:** RESOLVED
**Severity:** MAJOR → **N/A**
**Resolution:** V12 §3.3 renamed to principal-chain selection.

#### D-005 — Continuous-temperature derivatives unrealizable
**Status:** RESOLVED with caveat
**Severity:** MAJOR → **MINOR**
**Resolution:** V12 §13 specifies finite-difference doctrine, second-derivative warnings, common random numbers.
**Caveat:** Research agent recommended score-function (REINFORCE) gradients and pathwise/reparameterization estimators (Gumbel-softmax, Concrete) as superior to finite differences. V12 took the simpler path. Acceptable for constitution-level doc, weak for experiments paper. Upgrade in V13 if pursuing temperature-sensitivity claims.

#### D-006 — Indicator-based estimator vs P4 prose claim
**Status:** RESOLVED
**Severity:** MINOR → **N/A**
**Resolution:** V12 §11 reframes math as support mass and explicitly distinguishes from probability.

#### D-007 — Black-box utility components in pursuit policy
**Status:** PARTIAL
**Severity:** MAJOR → **MINOR**
**Resolution:** V12 §15 decomposes uncertainty into six typed components with remedy routing.
**Residual:** ProofGain, CoverageGain still not given functional definitions in V12. See D-NEW-2.

#### D-008 — Σ_spread ≈ kernel bandwidth (KDE connection)
**Status:** UNADDRESSED
**Severity:** MINOR
**Action required:** V13 either acknowledges connection to adaptive KDE / nearest-neighbor bandwidth selection (Silverman, Loader), or specifies the spread-control structure with explicit rationale.

#### D-009 — Model-correlation absent from §2 estimator
**Status:** PARTIAL
**Severity:** MINOR
**Resolution:** V12 §7 includes U_model as named uncertainty component.
**Residual:** §4.3 support estimator does not account for trajectory non-independence within a regime. Sampling n times from one model does not give n independent estimates. Add effective-sample-size correction analogous to §13 dependence-aware corroboration weighting, or vary model family across ρ explicitly.

#### D-010 — Lane A/B/C undefined
**Status:** UNADDRESSED in formal core
**Severity:** MINOR
**Action required:** Either define lanes explicitly (proof-capable / corroborative / hypothesis-only), or remove the term from the spec. Currently referenced in V11 §2.1 and V12 §15 but never enumerated.

#### D-011 — OOD calibration domain undefined
**Status:** PARTIAL
**Severity:** MINOR
**Resolution:** V12 §11 mentions per-query-class calibration.
**Residual:** No OOD detection mechanism. V13 should note recursive nature of OOD detection and recommend conformal-prediction-based approaches.

#### D-012 — "Posterior" colloquial drift
**Status:** RESOLVED
**Resolution:** V12 Appendix A bans "posterior" in formal core.

### 4.2 Research-agent-originated defects (status post-V12)

#### D-research-1 — "Chase" terminology collision with database theory
**Status:** RESOLVED
**Severity:** CRITICAL → **N/A**
**Resolution:** V12 §3.4 renamed to evidence pursuit loop / forward-chaining closure.

#### D-research-2 — Missing 8 categories of citations
**Status:** PROMISE WITHOUT DELIVERY
**Severity:** MAJOR
**Resolution:** V12 §21 acknowledges all 8 categories.
**Residual:** Not a single specific paper cited. ~40 specific citations from research agent must be incorporated before publication. See §7 of this Codex for the consolidated bibliography.

#### D-research-3 — DeepDive/Fonduer comparison missing
**Status:** PROMISE WITHOUT DELIVERY
**Severity:** MAJOR
**Resolution:** V12 §2 names DeepDive/Fonduer as "explicit neighbor."
**Residual:** No comparison table, no positioning statement, no analysis. Two-page comparison subsection required for any KBC/IR venue submission. See §6 D-2026-04 for the decision.

#### D-research-4 — Lindley EIG opportunity unrealized
**Status:** PARTIAL
**Severity:** MINOR
**Resolution:** V12 §12 names "expected ambiguity reduction" as target.
**Residual:** Highest-leverage technical opportunity in the architecture and V12 still hasn't taken it. The §12 proxies are all approximations or bounds on EIG under specific assumptions. Saying so explicitly would tie proxies to named target via existing literature (MacKay 1992, Houlsby BALD 2011).

### 4.3 V12-originated defects (NEW)

#### D-NEW-1 — Z_S, w(·), u_i, δ_ij all template-only
**Severity:** MAJOR
**Lane:** Lane 1 L1.1 + Lane 1 L1.3 + Lane 3 L3.2
**Issue:** The three load-bearing equations of V12 (§4.3 Claim Support Field, §4.6 Effective Corroboration, §8 Closure Objective) are all stated at template level. Z_S is undefined. w(r,c,q,N,ρ) is undefined as a function. u_i and δ_ij are undefined as functions. **Two engineers building from V12 alone will produce two different systems.**
**Action required for V13:** Lock down explicit functional forms with worked examples. Recommended choices:
- Z_S = total weighted support across candidate claims (yields per-query discrete distribution; absolute scale meaningful within-query only)
- w(r,c,q,N,ρ) = G(c,N) · Q(c) · A(r,N,ρ) where G is grounding score, Q is normalization quality, A is admissibility under regime
- u_i = grounding-weighted utility of evidence item i
- δ_ij = saturation function applied to typed-edge-weight + textual-overlap penalty

#### D-NEW-2 — Ambiguity functional H allowed to be six things
**Severity:** MINOR
**Lane:** Lane 1 L1.5
**Issue:** V12 §12 allows H to be "support entropy, JS divergence across regimes, expected calibrated risk, conflict count, coverage gap, abstention probability." Constitution-level allowing-anything means implementations diverge unpredictably.
**Action required:** Pick a default H. Recommended: entropy of grounded support over closure-relevant claims. Implementations may override but the default ties to Lindley EIG via Houlsby BALD 2011.

#### D-NEW-3 — §8 expected-loss closure uncomputable
**Severity:** MINOR
**Lane:** Lane 1 L1.10
**Issue:** a* = argmin_a E[L(a,θ;k) | evidence] requires posterior over θ that V12 explicitly disclaimed in §4.3. The expression is a wish, not an algorithm.
**Action required:** Reformulate around expected loss under the support distribution. Alternative: lean on conformal coverage-loss framework (Angelopoulos & Bates 2023) which doesn't require a posterior.

#### D-NEW-4 — Gibbs-posterior appendix opens new exposure
**Severity:** MINOR
**Lane:** Lane 1 L1.2
**Issue:** §4.4 extension is technically clean but invites the question "if Gibbs is principled, why isn't it default?" with no good answer.
**Action required:** Either commit to one Gibbs instantiation (e.g., descriptive-status queries with uniform prior + grounding-derived likelihood), or remove the appendix. Don't tease.

#### D-NEW-5 — §22 numbering off-by-one
**Severity:** NIT
**Resolution:** Fixed in this Codex §2.4.

### 4.4 Cross-cutting weaknesses identified by reviewer simulation

#### W-1 — Zero empirical content
**Severity:** PUBLICATION-FATAL at any peer-reviewed venue
**Lane:** Lane 2 L2.1
**Action:** Three required ablations on three public datasets before any submission. See §6 D-2026-05.

#### W-2 — Narrowed novelty claim undefended
**Severity:** MAJOR
**Lane:** Lane 2 L2.2
**Issue:** "Integrated synthesis is the contribution" is the right move but undefended without empirics.
**Action:** Empirics close this gap. Same fix as W-1.

#### W-3 — Falsifiability statement absent
**Severity:** MINOR
**Lane:** Lane 2 L2.2
**Action:** Add explicit "what observation would refute the framework" subsection.

#### W-4 — Ethics/risk section absent
**Severity:** MAJOR for ML/NLP venues
**Lane:** Lane 2 L2.3
**Action:** Section 9 paper templates include ethics scaffolding with required citations (Bender, Birhane, Selbst, Ajunwa, Green) and EU/US compliance mapping.

<!-- END FILE -->

---

<!-- FILE: codex/04_audits/v11_audit.md -->

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

**The wedge to ship first (working name candidates):** `coroborate`, `argus-rerank`, `provrank`. ~500 lines of Python. Standalone PyPI library + MCP server (`argus.mcp`) + LangChain partner package + LlamaIndex integration.

**License:** Apache 2.0 + DCO-only contributions. (Every BSL/SSPL/FSL relicense in last 3 years produced community fork: OpenSearch, OpenTofu, Valkey.)

**Documentation:** MkDocs Material or Mintlify. Three pillars: concepts / how-to cookbook / API reference. 3-5 launch notebooks all Colab-runnable in <5 min. Publish `llms.txt` at root.

**Community:** Defer Discord. GitHub Issues + Discussions only for first 3 months. Solo maintainer at financial firm with full-time job will burn out moderating.

**Twitter is not optional:** ~1-2 substantive threads/week for 12 months minimum. Without this the wedge ships into silence.

**18-month canonization probability conditional on disciplined execution:** 15-25% (high relative to baseline rate for new RAG projects, well under 5%).

<!-- END FILE -->

---

<!-- FILE: codex/05_decisions.md -->

## 6. Decision log — what's been settled and why

Format: `D-YYYY-NN | DECIDED: <decision> | RATIONALE: <reason> | ALTERNATIVES_REJECTED: <what we said no to>`

### D-2026-01 | Wedge first, full system second
**Decided:** Ship dependence-aware reranker as standalone PyPI package + MCP server before publishing the integrated ARGUS architecture. The full system follows as a 12-month follow-on, citing the wedge as established work.
**Rationale:** Lane 4 publication research and canonization research converged on this. Every canonical AI infrastructure project of 2022–2026 launched a wedge first (FlashAttention before Mamba, Snorkel labeling functions before full platform, Instructor patch before framework). Solo engineer at financial firm with day job cannot ship full integrated system in 18 months.
**Alternatives rejected:** Single big-bang release of full ARGUS (timeline infeasible); academic-track paper first (no empirical content, would be desk-rejected); CACM Practice essay first (no underlying artifact to point to, becomes vapor).

### D-2026-02 | Apache 2.0 + DCO only
**Decided:** License the wedge and full ARGUS under Apache 2.0. Require DCO sign-off on contributions. No CLA.
**Rationale:** Every BSL/SSPL/FSL relicense in last 3 years (MongoDB, Elastic, HashiCorp, Redis) produced community-led fork. Apache 2.0 patent grant matters in forensic-evidence territory. DCO over CLA because copyright assignment signals vendor-product-in-disguise; CNCF projects all use DCO. Financial-sector legal review prefers explicit patent clauses.
**Alternatives rejected:** MIT (no patent grant); BSL/SSPL (community-fork risk); CC0 (no patent grant, weaker provenance for derivative work).

### D-2026-03 | Defer Discord, foreground Twitter
**Decided:** GitHub Issues + Discussions only at launch and through month 6 minimum. No Discord. Solo maintainer commits to 1-2 substantive Twitter/X threads per week for 12 months.
**Rationale:** Solo engineer with full-time job at financial firm cannot moderate Discord without burnout. FlashAttention, vLLM (until late 2024), GraphRAG canonized without Discord. Twitter megaphone is non-optional — Instructor (Jason Liu), llm CLI (Simon Willison), Mamba (Tri Dao) all required consistent personal-account presence to canonize.
**Alternatives rejected:** Launch with Discord (burnout risk); rely on GitHub alone (insufficient distribution).

### D-2026-04 | DeepDive comparison required, not optional
**Decided:** Every paper or major artifact about ARGUS must include explicit positioning against DeepDive/Fonduer. Two-page comparison table minimum.
**Rationale:** Lane 2 reviewer simulation and Lane 4 publication research both flagged this. DeepDive covers 3 of 4 PRC pillars and is unavoidable as the closest comparable system. Every KBC/IR/database reviewer will demand this. DeepDive being maintenance-mode-dead is favorable but only if explicitly addressed.
**Alternatives rejected:** Treat as one of many neighbors (insufficient); ignore (publication-fatal).

### D-2026-05 | Three ablations, three datasets, before any peer-review submission
**Decided:** No peer-review submission until three ablations on Stock + RAMDocs + FEVEROUS are run, plus DeepDive baseline on Stock for KBC venues. arXiv preprint may go up earlier.
**Rationale:** Lane 2 universal verdict: zero empirics = reject everywhere. Lane 4: this specific dataset selection ties dependence-aware-corroboration claim to its strongest case (Stock has source copying), most-current conflict benchmark (RAMDocs Apr 2025), and forensic-evidence-style verification (FEVEROUS).
**Alternatives rejected:** Submit V12 as-is (publication-fatal); use only synthetic benchmarks (less defensible); use only the actual KKR data (legal/disclosure problems).

### D-2026-06 | "Theorem hygiene" stays as a deliberate posture
**Decided:** Keep V12 §19 / §26 statement-class taxonomy. Do not promote any current claim to "theorem" status without proof.
**Rationale:** Lane 2 noted this is rare in LLM-systems specs and Lane 1 noted it as exemplary. Lipton & Steinhardt 2018 explicitly called for this. Comparable systems papers (DeepDive, Fonduer, Self-RAG, GraphRAG, HippoRAG, FLARE, Atlas) contain zero formal theorems in main text — adding more theory does not earn credit, and theory hygiene is the differentiator.
**Alternatives rejected:** Add formal theorems to look more rigorous (counterproductive); abandon the taxonomy as too academic (loses the credibility move).

### D-2026-07 | Math layer (§4) lockdown required for V13
**Decided:** Before V13 ships, lock explicit functional forms for Z_S, w(r,c,q,N,ρ), u_i, δ_ij, H. Recommended choices in §4 D-NEW-1.
**Rationale:** Lane 3 found the math layer is the unbuildable region of V12. Two engineers building from V12 alone produce different systems. Constitution-level allowing-anything is not a constitution.
**Alternatives rejected:** Leave as templates (engineering divergence); replace with full Bayesian framework (too heavy); abandon math layer entirely (loses the architectural claim).

### D-2026-08 | KKR use case stays internal forever
**Decided:** The actual day-job evidence and use case never appears in any public artifact. Public demos use Enron, OpenAlex, CourtListener, public benchmarks only.
**Rationale:** Legal/comms clearance for forensic-workplace-evidence framing at a financial firm is impractical. EU AI Act Annex III §4 makes this high-risk; California ADMT regulations require pre-use risk assessment; NYC Local Law 144 may apply to NYC-resident employees; Article 5(1)(f) prohibits emotion recognition in workplace. Anything published becomes potential discovery material in employment litigation.
**Alternatives rejected:** Publish sanitized internal case study (clearance friction too high); use synthetic-but-similar internal-feeling examples (still triggers IP/clearance review); attempt anonymized publication (re-identification risk too high).

### D-2026-09 | "Dependence-aware corroboration" is the named primitive
**Decided:** The phrase to spread is "dependence-aware corroboration" or "dependence-aware reranking" depending on context. This is the wedge name and the canonical reference.
**Rationale:** Canonization research found memorable phrases beat compound nouns. "Dependence-aware corroboration" is both googleable and not currently claimed by any project. Ties directly to truth-discovery lineage (Dong 2009) which establishes intellectual provenance.
**Alternatives rejected:** "Anti-double-counting" (not technical enough); "Source-correlation-aware retrieval" (too long); "Trust-correlated retrieval" (collides with web-of-trust literature).

### D-2026-10 | Codex format: single file, mobile-first, splittable
**Decided:** Deliver consolidation as single ARGUS_CODEX.md with HTML-comment file markers and a split script. Optimize for end-to-end phone reading, second-pass desktop split into repo structure.
**Rationale:** Director explicitly chose mobile-portability over multi-file delivery to prevent fragmentation during the phone-to-GitHub transit.
**Alternatives rejected:** Multi-file delivery (mobile fragmentation); GitHub Gist (loses cross-references); Google Doc (proprietary, not version-controllable).

<!-- END FILE -->

---

<!-- FILE: codex/06_citations.md -->

## 7. Consolidated bibliography

Organized by category. Each entry is a single line for grep-ability. Use this as the master bib for any future paper.

### 7.1 Self-consistency and prompt ensembling
- Wang, X. et al. 2022. "Self-Consistency Improves Chain of Thought Reasoning." arXiv:2203.11171. ICLR 2023.
- Chen, X. et al. 2023. "Universal Self-Consistency for Large Language Model Generation." arXiv:2311.17311.
- Aggarwal, P. et al. 2023. "Adaptive Consistency." arXiv:2305.11860. EMNLP 2023.
- Li, Y. et al. 2023. "DiVeRSe." arXiv:2206.02336. ACL 2023.
- Wang, H. et al. 2024. "Soft Self-Consistency." arXiv:2402.13212. ACL 2024.
- Pitis, S. et al. 2023. "Boosted Prompt Ensembles." arXiv:2304.05970.
- Korikov, A. et al. 2025. "Batched Self-Consistency for Ranking." arXiv:2505.12570.
- Kuhn, L. et al. 2023. "Semantic Uncertainty." ICLR 2023.
- Knappe, T. et al. 2024. "Semantic Self-Consistency." arXiv:2410.07839.
- Taubenfeld, A. et al. 2025. "Confidence Improves Self-Consistency in LLMs." arXiv:2502.06233. ACL 2025.

### 7.2 Truth discovery and source dependence
- Yin, X., Han, J., Yu, P.S. 2008. "Truth Discovery with Multiple Conflicting Information Providers on the Web." IEEE TKDE 20(6).
- Dong, X.L., Berti-Equille, L., Srivastava, D. 2009. "Integrating Conflicting Data: The Role of Source Dependence." PVLDB 2(1).
- Dong, X.L., Berti-Equille, L., Srivastava, D. 2009. "Truth Discovery and Copying Detection in a Dynamic World." PVLDB 2(1).
- Dong, X.L. et al. 2010. PVLDB 3.
- Pochampally, R. et al. 2014. "Fusing Data with Correlations." SIGMOD 2014.
- Galland, A. et al. 2010. WSDM 2010.
- Dong, X.L. et al. 2015. "Knowledge-Based Trust." PVLDB 8(9).
- Pasternack, J., Roth, D. 2010. "Knowing What to Believe (When You Already Know Something)." COLING 2010.
- Li, Y. et al. 2012. "Resolving Conflicts in Heterogeneous Data by Truth Discovery and Source Reliability Estimation." VLDB 2012.

### 7.3 Bayesian networks and evidential reasoning
- Schum, D.A. 1994. *The Evidential Foundations of Probabilistic Reasoning*. Northwestern UP.
- Bovens, L., Hartmann, S. 2003. *Bayesian Epistemology*. Oxford UP.
- Pearl, J. 1988. *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann.
- Pearl, J. 2009. *Causality* 2e. Cambridge UP. DOI: 10.1017/CBO9780511803161.
- Fenton, N., Neil, M. 2018. *Risk Assessment and Decision Analysis with Bayesian Networks* 2e. CRC. DOI: 10.1201/b21982.
- Fenton, N., Neil, M., Lagnado, D. 2013. "A General Structure for Legal Arguments About Evidence Using Bayesian Networks." Cognitive Science 37(1).
- Kadane, J., Schum, D. 1996. *A Probabilistic Analysis of the Sacco and Vanzetti Evidence*. Wiley.
- Koller, D., Friedman, N. 2009. *Probabilistic Graphical Models*. MIT Press.
- Yager, R. 2009. "Generalized Dempster-Shafer for Dependent Sources." IJGS 38(5).
- Juchli, P., Biedermann, A., Taroni, F. 2025. *AI & Law*.
- Taroni, F., Aitken, C., Garbolino, P., Biedermann, A. 2014. *Bayesian Networks for Probabilistic Inference and Decision Analysis in Forensic Science* 2e. Wiley.

### 7.4 Calibration and selective prediction
- Guo, C. et al. 2017. "On Calibration of Modern Neural Networks." ICML 2017. arXiv:1706.04599.
- Desai, S., Durrett, G. 2020. "Calibration of Pre-trained Transformers." EMNLP 2020. arXiv:2003.07892.
- Kadavath, S. et al. 2022. "Language Models (Mostly) Know What They Know." arXiv:2207.05221.
- Lin, S., Hilton, J., Evans, O. 2022. "Teaching Models to Express Their Uncertainty in Words." TMLR. arXiv:2205.14334.
- Tian, K. et al. 2023. "Just Ask for Calibration." EMNLP 2023. arXiv:2305.14975.
- Jiang, Z. et al. 2021. "How Can We Know When Language Models Know?" TACL. DOI: 10.1162/tacl_a_00407.
- Geng, J. et al. 2024. "Calibration Survey." arXiv:2311.08298.
- Kendall, A., Gal, Y. 2017. "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?" arXiv:1703.04977.
- Hüllermeier, E., Waegeman, W. 2021. "Aleatoric and Epistemic Uncertainty in Machine Learning." Mach. Learn. 110(3).
- Hou, B. et al. 2024. "Decomposing Uncertainty for LLMs through Input Clarification Ensembling." ICML 2024. arXiv:2311.08718.

### 7.5 Conformal prediction for LLMs
- Angelopoulos, A., Bates, S. 2023. "Conformal Prediction: A Gentle Introduction." FnT Mach. Learn. 16(4). arXiv:2107.07511.
- Quach, V. et al. 2024. "Conformal Language Modeling." ICLR 2024. arXiv:2306.10193.
- Mohri, C., Hashimoto, T. 2024. "Language Models with Conformal Factuality Guarantees." ICML 2024. arXiv:2402.10978.
- Cherian, J., Gibbs, I., Candès, E. 2024. NeurIPS 2024. arXiv:2406.09714.
- Vovk, V., Gammerman, A., Shafer, G. 2022. *Algorithmic Learning in a Random World* 2e. Springer.

### 7.6 RAG and active retrieval
- Jiang, Z. et al. 2023. "Active Retrieval Augmented Generation (FLARE)." EMNLP 2023. arXiv:2305.06983.
- Asai, A. et al. 2024. "Self-RAG." ICLR 2024. arXiv:2310.11511.
- Trivedi, H. et al. 2023. "IRCoT." ACL 2023. arXiv:2212.10509.
- Yao, S. et al. 2023. "ReAct." ICLR 2023. arXiv:2210.03629.
- Yan, S. et al. 2024. "CRAG." arXiv:2401.15884.
- Edge, D. et al. 2024. "GraphRAG." arXiv:2404.16130.
- Gutiérrez, B. et al. 2024. "HippoRAG." NeurIPS 2024. arXiv:2405.14831.
- Izacard, G. et al. 2023. "Atlas." JMLR 24. arXiv:2208.03299.
- Shi, W. et al. 2024. "REPLUG." NAACL 2024. arXiv:2301.12652.
- Hwang, K. et al. 2024. "RAG with Estimation of Source Reliability." EMNLP 2025. arXiv:2410.22954.

### 7.7 Conflict-aware RAG
- Wang, H. et al. 2025. "Retrieval-Augmented Generation with Conflicting Evidence (RAMDocs/MADAM-RAG)." arXiv:2504.13079.
- Su, J. et al. 2024. "ConflictBank." NeurIPS 2024 D&B.
- Wang, F. et al. 2024. "Astute RAG."
- Jiayang, C. et al. 2024. "ECON." EMNLP 2024.
- Longpre, S. et al. 2021. Entity-substitution conflict.

### 7.8 Bayesian experimental design / EIG
- Lindley, D.V. 1956. "On a Measure of the Information Provided by an Experiment." Annals of Mathematical Statistics 27(4).
- MacKay, D.J.C. 1992. "Information-Based Objective Functions for Active Data Selection." Neural Computation.
- Chaloner, K., Verdinelli, I. 1995. "Bayesian Experimental Design: A Review." Statistical Science.
- Houlsby, N. et al. 2011. "Bayesian Active Learning by Disagreement (BALD)."
- Foster, A. et al. 2021. "Deep Adaptive Design." ICML 2021.

### 7.9 Database theory: chase, provenance
- Maier, D., Mendelzon, A.O., Sagiv, Y. 1979. "Testing Implications of Data Dependencies." ACM TODS 4(4):455-469. DOI: 10.1145/320107.320115.
- Aho, A.V., Beeri, C., Ullman, J.D. 1979. "The Theory of Joins in Relational Databases." ACM TODS 4(3):297-314.
- Fagin, R., Kolaitis, P.G., Miller, R.J., Popa, L. 2005. "Data Exchange: Semantics and Query Answering." TCS 336(1).
- Fagin, R., Kolaitis, P.G., Popa, L. 2005. "Data Exchange: Getting to the Core." ACM TODS 30(1).
- Cheney, J., Chiticariu, L., Tan, W.-C. 2009. "Provenance in Databases: Why, How, and Where." FnT Databases 1(4). DOI: 10.1561/1900000006.
- Buneman, P., Khanna, S., Tan, W.-C. 2001. "Why and Where: A Characterization of Data Provenance." ICDT 2001.
- Green, T., Karvounarakis, G., Tannen, V. 2007. "Provenance Semirings." PODS 2007. DOI: 10.1145/1265530.1265535.
- W3C 2013. "PROV-DM: The PROV Data Model." W3C Recommendation.
- C2PA 2024. "Coalition for Content Provenance and Authenticity Specifications."

### 7.10 Knowledge base construction and DeepDive lineage
- Niu, F. et al. 2012. "DeepDive: Web-Scale Knowledge-Base Construction Using Statistical Learning and Inference." VLDS 2012.
- Shin, J. et al. 2015. "Incremental Knowledge Base Construction Using DeepDive." PVLDB 8(11). arXiv:1502.00731.
- Zhang, C. et al. 2017. "DeepDive: Declarative Knowledge Base Construction." CACM May 2017.
- Wu, S. et al. 2018. "Fonduer: Knowledge Base Construction from Richly Formatted Data." SIGMOD 2018.
- Ratner, A. et al. 2017. "Snorkel: Rapid Training Data Creation with Weak Supervision." VLDB 2017.

### 7.11 Temperature and test-time scaling
- Wu, Z., Mirhoseini, A., Tambe, M. 2025. "On the Role of Temperature Sampling in Test-Time Scaling." arXiv:2510.02611.
- Renze, M. 2024. "Temperature Sweep T∈[0,1]." arXiv:2402.05201.
- Glynn, P.W. 1990. "Likelihood Ratio Gradient Estimation." CACM.
- Williams, R.J. 1992. "REINFORCE."
- Schulman, J. et al. 2015. "Stochastic Computation Graphs." NeurIPS 2015. arXiv:1506.05254.
- Jang, E. et al. 2017. "Gumbel-Softmax." ICLR 2017. arXiv:1611.01144.
- Maddison, C. et al. 2017. "Concrete Distribution." ICLR 2017. arXiv:1611.00712.

### 7.12 Responsible AI for forensic / workplace systems
- Bender, E., Gebru, T., McMillan-Major, A., Shmitchell, S. 2021. "On the Dangers of Stochastic Parrots." FAccT 2021.
- Birhane, A. 2021. "Algorithmic Injustice: A Relational Ethics Approach." Patterns 2(2):100205.
- Selbst, A. et al. 2019. "Fairness and Abstraction in Sociotechnical Systems." FAccT 2019.
- Ajunwa, I. 2023. *The Quantified Worker*. Cambridge UP.
- Ajunwa, I. 2023. "Automated Governance." 101 N.C. L. Rev. 355.
- Green, B. 2022. "The Flaws of Policies Requiring Human Oversight of Government Algorithms." Computer Law & Security Review 45:105681.
- Crawford, K., Whittaker, M. (AI Now Institute). Various, "Algorithmic Management."
- Li, J. et al. 2024. "A Survey on LLM-as-a-Judge." arXiv:2411.15594.
- Maloyan, A. et al. 2025. "Vulnerability of LLM-as-a-Judge to Prompt Injection." arXiv:2505.13348.
- Lipton, Z., Steinhardt, J. 2018. "Troubling Trends in Machine Learning Scholarship." CACM. arXiv:1807.03341.

### 7.13 Reading list — must-read for V13 author
Top 10 papers to read before any V13 work:
1. Schum 1994 *Evidential Foundations* — for the dependence vocabulary
2. Dong/Berti-Equille/Srivastava 2009 PVLDB — for source-copying detection
3. Pochampally et al. 2014 SIGMOD — for cluster-level corrections beyond pairwise
4. Shin et al. 2015 PVLDB DeepDive Incremental — primary structural template
5. Gutiérrez et al. 2024 NeurIPS HippoRAG — secondary structural template
6. Wang et al. 2022 ICLR Self-Consistency — foundational comparison
7. Jiang et al. 2023 EMNLP FLARE — closest active-retrieval work
8. Kadavath et al. 2022 — calibration methodology baseline
9. Mohri & Hashimoto 2024 ICML — closest conformal-LM ancestor
10. Edge et al. 2024 GraphRAG — closest published architecture

<!-- END FILE -->

---

<!-- FILE: codex/wedges/wedge1_dependence_reranker.md -->

## 8. Wedge templates — what to build first

### 8.1 Wedge 1 — Dependence-aware reranker

**Status:** PRIMARY WEDGE. This is the first artifact to ship.

**One-line definition:** A standalone Python library that, given a query and a set of retrieved documents, computes per-document dependence weights and produces a re-ranked list with calibrated confidence on the underlying claim.

**Naming candidates** (check PyPI and GitHub before committing):
- `coroborate` (preferred — phonetic, googleable, evokes "corroborate" with a twist)
- `argus-rerank` (clear but generic)
- `provrank` (provenance-aware ranking; clean)
- `evidently-rerank` — REJECTED (collides with existing observability tool)

**Target installation experience:**
```bash
pip install coroborate
```

```python
from coroborate import DependenceAwareReranker

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
- MCP server (`coroborate.mcp`) — both stdio and Streamable HTTP
- LangChain partner package: `langchain-coroborate` implementing `BaseDocumentCompressor`
- LlamaIndex integration: `llama-index-postprocessor-coroborate`

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
- [ ] PyPI package published (`pip install coroborate` works)
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

<!-- END FILE -->

<!-- FILE: codex/wedges/wedge2_provenance_loader.md -->

### 8.2 Wedge 2 — Provenance-tagged document loader

**Status:** SECONDARY WEDGE. Ship at month 7-9 if Wedge 1 has crossed 2k stars and external pull is real. Skip if Wedge 1 is below threshold.

**One-line definition:** A document loader for organizational evidence formats (mbox, EDRM XML, PST, MS Graph exports, JIRA exports, Slack exports, Zoom transcripts, log bundles) that preserves cryptographic chain-of-custody and lineage metadata in a stratified output format.

**Why this is the second wedge:** No comparable open-source library exists. Aleph's open-source sunset (Dec 31, 2025) leaves a vacuum. Investigative journalism, fact-checking, and forensic-evidence communities all need this. Plays directly to ARGUS strata §2.3.

**Surface:**
- Python library: `pip install argus-loaders`
- CLI: `argus-load --source-type mbox --input mailbox.mbox --output stratum/`
- Output format: ARGUS strata-compliant directory tree with PROV-DM lineage records

**Naming:** `argus-loaders` (carries ARGUS brand to wedge 2 deliberately)

**Target build size:** ~2,000 lines (heavier than Wedge 1 because format coverage is the value)

**Demo target:** Enron mbox → ARGUS strata in one command, verifiable chain-of-custody hashes match across runs

<!-- END FILE -->

<!-- FILE: codex/wedges/wedge3_calibration_layer.md -->

### 8.3 Wedge 3 — Calibration layer for forensic claims

**Status:** TERTIARY WEDGE. Ship at month 12+ as part of full ARGUS reference architecture release, not as a standalone first.

**Why not first:** Calibration requires labeled validation data, which requires the rest of the system to be running and a real query workload to score. As Lane 3 noted, this is NEEDS_PROTOTYPE_FIRST.

**One-line definition:** A calibrator that maps support + grounding + dependence + uncertainty features into calibrated decision probabilities for forensic claims, with per-query-class evaluation via Brier / ECE / reliability diagrams / selective risk.

**Closest published cousin:** Mohri & Hashimoto 2024 (Conformal LM Factuality Guarantees). Differentiate by: (a) per-query-class calibration, (b) integration with dependence-aware corroboration features, (c) selective-prediction interface.

**Defer until V13 ships and the wedge ecosystem is in place.**

<!-- END FILE -->

---

<!-- FILE: codex/papers/paper1_workshop_template.md -->

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

<!-- END FILE -->

<!-- FILE: codex/papers/paper2_reference_arch.md -->

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

<!-- END FILE -->

<!-- FILE: codex/papers/paper3_practitioner_essay.md -->

### 9.3 Paper 3 — Practitioner essay template

**Target venues (in priority order):**
1. **CACM Practice section** (≤6,000 words, code encouraged, recently rebooted under EiC Terence Kelly, pitch by email first)
2. **ACM Queue** (functionally invitation-only; arrives via the arXiv→noticed pattern)
3. **IEEE Software Insights / Pragmatic Architect column** (~6 pages, practitioner-friendly)
4. **InfoQ writeup paired with QCon AI talk** (no peer review; high practitioner reach)
5. **Anthropic-style engineering blog post** (own domain or Substack; gets canonical via cross-citation)

**Length:** 5,000-6,000 words, no formal mathematics

**Title candidates:**
- "Building ARGUS: Lessons from a Forensic-Grade Truth Engine"
- "Dependence-Aware Corroboration in Practice: Why Your RAG Is Lying to You"
- "Patterns for Truth-Oriented Retrieval: Notes from the Trenches"

**Section skeleton:**

#### Opening (400 words)
- The hook: a real but anonymized story of corroboration inflation
- "47 documents say the same thing. Three of them know it firsthand. The other 44 are echoes."
- Why this matters now: enterprise RAG, fact-checking, investigative work, regulatory compliance

#### What we built and why (800 words)
- ARGUS in one paragraph (Codex §2.1)
- The pattern names: stratified evidence, dependence-aware corroboration, claim support field, evidence pursuit loop
- What problems it solves that vanilla RAG doesn't

#### Pattern 1: Stratified evidence (800 words)
- Why decision objects must not flow back to raw evidence
- The six-stratum layout (Codex §2.3)
- What goes wrong when stratification breaks (the "summary-of-summary-of-summary" problem)

#### Pattern 2: Dependence-aware corroboration (1,000 words)
- The truth-discovery lineage in plain English (Yin 2008, Dong 2009, in narrative form)
- The typed-edge taxonomy (§3.6)
- Worked example: FTX or citation-laundering case study
- Why this is the highest-leverage pattern for production RAG today

#### Pattern 3: Multi-regime claim support (600 words)
- Self-consistency in plain English
- Why one regime isn't enough
- The Claim Support Field as estimator (no math, narrative only)

#### Pattern 4: Calibrated closure (800 words)
- The difference between "the model is confident" and "the system should commit"
- Per-query-class calibration
- When to abstain vs. close vs. escalate

#### Pattern 5: Evidence pursuit loop (500 words)
- Active retrieval as expected ambiguity reduction
- Connection to Lindley EIG (one paragraph; no formulas)
- The stopping rule

#### What we got wrong (700 words)
- Honest accounting: the V11 → V12 evolution as a story
- "We called things 'posteriors' that weren't"
- "We used 'tensor' to mean 'function with multiple inputs'"
- The theorem-hygiene practice as a corrective discipline
- This section is the credibility move — no other practitioner essay does this well

#### What we still don't know (400 words)
- Open problems list (subset of Paper 2 §7)
- Honest limitations
- Invitation to collaborators

#### How to use this (300 words)
- Pointer to GitHub (Wedge 1)
- Quickstart code excerpt
- "Try it on your own evidence" call to action

#### About this work (100 words)
- One-paragraph bio
- Acknowledgments

**Voice notes:**
- First person plural ("we built") — even if solo, sounds like a team practice
- Concrete examples beat abstract claims
- Pattern names in **bold** on first introduction so they stick
- Avoid "novel," "innovative," "breakthrough" — let readers conclude, don't tell them
- Imitate: Dan McKinley's Boring Technology Club essay, Marc Brooker's blog, Hellerstein's writing, Anthropic's "Building Effective Agents," Snorkel blog at its best

**Estimated effort:** 2-3 weeks of writing if Wedge 1 has shipped and the patterns have been used in anger.

<!-- END FILE -->

---

<!-- FILE: codex/99_split_script.sh -->

## 10. Split script — desktop-side conversion to repo structure

When you're ready to convert this single Codex into the multi-file repo structure, save the script below as `split_codex.sh`, place it in the same directory as `ARGUS_CODEX.md`, run `bash split_codex.sh`, and commit the resulting `codex/` directory to GitHub.

```bash
#!/usr/bin/env bash
# split_codex.sh — extract ARGUS_CODEX.md into the multi-file repo structure
#
# Usage: bash split_codex.sh [path-to-ARGUS_CODEX.md]
#        Defaults to ./ARGUS_CODEX.md if no argument given.
#
# Produces a codex/ directory tree per the manifest in Section 1 of the Codex.
# Portable across Linux (gawk) and macOS (BSD awk) — uses pure bash + sed.

set -euo pipefail

CODEX="${1:-ARGUS_CODEX.md}"

if [[ ! -f "$CODEX" ]]; then
  echo "ERROR: $CODEX not found" >&2
  exit 1
fi

current_file=""
while IFS= read -r line; do
  if [[ "$line" =~ \<!--\ FILE:\ ([^[:space:]]+)\ --\> ]]; then
    current_file="${BASH_REMATCH[1]}"
    mkdir -p "$(dirname "$current_file")"
    : > "$current_file"   # truncate or create empty
    continue
  fi
  if [[ "$line" =~ \<!--\ END\ FILE\ --\> ]]; then
    current_file=""
    continue
  fi
  if [[ -n "$current_file" ]]; then
    printf '%s\n' "$line" >> "$current_file"
  fi
done < "$CODEX"

echo "Split complete. Generated tree:"
find codex -type f | sort
```

**To make the result a proper Git repo:**

```bash
cd codex
git init
git add .
git commit -m "Initial Codex import from ARGUS_CODEX.md v1.0"
# Then create the GitHub repo and push:
# git remote add origin git@github.com:VerbalChainsaw/argus-codex.git
# git branch -M main
# git push -u origin main
```

**Recommended .gitignore:**
```
.DS_Store
*.swp
__pycache__/
.venv/
node_modules/
build/
dist/
*.egg-info/
```

<!-- END FILE -->

---

## End of Codex

**Document version:** 1.0
**Date:** 2026-04-26
**Status:** Initial consolidation. Living document — update the defect register (§4) and decision log (§6) as work proceeds.

**For future Claude (or future you):** to extend this Codex without breaking it, add new sections as new file blocks (use the same `&lt;!-- FILE: codex/your-path --&gt;` ... `&lt;!-- END FILE --&gt;` pattern shown throughout this document). Each addition should also get an entry in the manifest (§1) and, if it represents a settled choice, a new entry in the decision log (§6). Treat this document the way you would treat a well-organized monorepo — add, don't restructure.

**Carry-forward priority order:**
1. Read this end-to-end on your phone (Codex purpose #2)
2. Run the split script when at desktop, push to GitHub (Codex purpose #1)
3. Pick Wedge 1 (§8.1) as the first artifact to build
4. Use Paper 1 template (§9.1) when writing the first peer-reviewed submission
5. Update §6 decisions as you make them
6. Resolve §4.3 D-NEW-1 before ARGUS V13 lockdown
