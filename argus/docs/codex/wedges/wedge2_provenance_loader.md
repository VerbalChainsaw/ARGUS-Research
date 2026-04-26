
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

