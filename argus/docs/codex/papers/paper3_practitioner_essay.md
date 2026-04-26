
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

