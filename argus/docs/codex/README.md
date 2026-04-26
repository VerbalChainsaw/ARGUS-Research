# ARGUS Codex (vendored)

This directory is the multi-file split of the **ARGUS Codex v1.0** — the
unified working document for the PRC + ARGUS architecture from which
**ARGUS-Rerank** (PyPI `argus-rerank`, import `argus_rerank`) is the first wedge artifact implemented in this repo.

The Codex is the source of truth for design decisions affecting this repo.
Treat it as a versioned constitution, not as code documentation.

## Files

```
00_README.md                         Why the Codex exists; what survived audit
01_architecture.md                   What ARGUS actually is (six layers)
02_v12_canonical_definitions.md      The formal core (locked terms)
03_defects.md                        Live defect register
04_audits/v11_audit.md               Original brutal scientific audit
05_decisions.md                      Decision log (D-2026-01..10)
06_citations.md                      Consolidated bibliography
99_split_script.sh                   The split script that produced this tree
papers/paper1_workshop_template.md   Wedge paper skeleton
papers/paper2_reference_arch.md      Reference architecture paper skeleton
papers/paper3_practitioner_essay.md  Practitioner essay skeleton
wedges/wedge1_dependence_reranker.md THIS REPO's spec
wedges/wedge2_provenance_loader.md   Future: argus-loaders
wedges/wedge3_calibration_layer.md   Future: full calibration layer
```

## Reading order if you are new

1. `00_README.md` — what this whole effort is
2. `wedges/wedge1_dependence_reranker.md` — the spec for what's in this repo
3. `01_architecture.md` — where this wedge fits in the larger picture
4. `05_decisions.md` — what's been settled and why

## Why this lives in the repo, not somewhere else

ARGUS Codex Decision **D-2026-10**: single-file mobile-portable Codex,
splittable on demand. We split into the repo so that:

1. The spec travels with the code under the same git history.
2. Future contributors can read the constitution without leaving the repo.
3. Any drift between the code and the spec is detectable via diff.

The Codex is updated additively per its own self-instructions (see end of
`00_README.md`). When changing a settled decision (§5), add a new entry; do
not edit prior ones.
