"""ARGUS-Rerank — dependence-aware reranking for retrieval-augmented generation.

This package (**import** ``argus_rerank``) implements Wedge 1 of the ARGUS / PRC architecture:
the dependence-aware reranker. See :mod:`argus_rerank.reranker` for the
top-level API and ``docs/codex/wedges/wedge1_dependence_reranker.md`` for
the full specification.

The named primitive is **dependence-aware corroboration**: aggregate evidence
in support of a claim while discounting correlated sources that quote,
mirror, summarize, or are derived from each other.

Public API
----------
- :class:`DependenceAwareReranker` — top-level reranker
- :class:`Document` — input document representation
- :class:`DependenceEdge` — typed dependence relation between two documents
- :class:`RankedDocument` — a document with computed weight and dependence summary
- :class:`RerankResult` — final reranker output

Status discipline (ARGUS Codex §3.10): every module-level docstring tags the
class of any mathematical or empirical statement it makes. This package contains
no theorems; it contains heuristics, engineering rules, and architecture-
conditional propositions.
"""

from argus_rerank.models import (
    DependenceEdge,
    DependenceEdgeType,
    Document,
    RankedDocument,
    RerankResult,
)
from argus_rerank.reranker import DependenceAwareReranker, RerankerConfig

__version__ = "0.1.0"

__all__ = [
    "DependenceAwareReranker",
    "RerankerConfig",
    "Document",
    "DependenceEdge",
    "DependenceEdgeType",
    "RankedDocument",
    "RerankResult",
    "__version__",
]
