
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

