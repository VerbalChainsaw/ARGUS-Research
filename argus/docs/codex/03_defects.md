
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

