# Changelog

All notable changes to **ARGUS-Rerank** (`argus-rerank` / `argus_rerank`) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial 0.1.0 alpha implementation of dependence-aware reranking.
- Pydantic models for `Document`, `DependenceEdge`, `RankedDocument`, `RerankResult`.
- Near-duplicate detection via SimHash + MinHash (`argus_rerank.near_duplicate`).
- Typed dependence-graph construction (`argus_rerank.dependence_graph`) following
  the ARGUS V12 §10 edge taxonomy.
- Copy-language detection via overlapping n-gram Jaccard
  (`argus_rerank.copy_detection`).
- Effective corroboration `C_eff` computation with logarithmic saturation
  (`argus_rerank.effective_corroboration`).
- Calibration layer with isotonic regression and Platt scaling
  (`argus_rerank.calibration`).
- Top-level `DependenceAwareReranker` API.
- Minimal CLI: `argus-rerank rerank --query ... --documents docs.json`.
- Comprehensive unit tests for each module.
- Apache 2.0 license + DCO contribution policy.

[Unreleased]: https://github.com/VerbalChainsaw/argus-rerank/compare/HEAD...HEAD
