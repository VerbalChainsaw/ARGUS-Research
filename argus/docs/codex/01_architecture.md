
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

