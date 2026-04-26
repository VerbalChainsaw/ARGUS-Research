
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

