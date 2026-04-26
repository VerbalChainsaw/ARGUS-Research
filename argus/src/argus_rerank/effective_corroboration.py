"""Effective corroboration C_eff and per-document weight computation.

Implements the ARGUS Codex §3.6 / V12 §4.6 template:

    C_eff(c) = Σᵢ uᵢ − Σᵢ<ⱼ δᵢⱼ

with the recommended functional forms from §4 D-NEW-1:

    uᵢ      = grounding-weighted utility of document i (default: 1.0 unless
              the upstream retrieval score or :attr:`Document.score` overrides)
    δᵢⱼ     = saturation function applied to the maximum-weighted dependence
              edge between i and j

Statement-class
---------------
Engineering rule. The exact functional forms here are recommended defaults and
will be locked down for V13 alongside ARGUS Codex defect D-NEW-1. The output
is calibrated downstream by :mod:`argus_rerank.calibration`, so absolute scale
errors here are absorbed by the calibrator.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import cast

import networkx as nx

from argus_rerank.models import DependenceEdge, DependenceEdgeType, Document


@dataclass(frozen=True)
class EffectiveCorroborationConfig:
    """Configuration for the C_eff computation."""

    edge_type_strength: dict[DependenceEdgeType, float] = field(
        default_factory=lambda: {
            DependenceEdgeType.MIRRORS: 1.00,
            DependenceEdgeType.DERIVED_FROM: 0.95,
            DependenceEdgeType.SUMMARY_OF: 0.90,
            DependenceEdgeType.QUOTE_OF: 0.75,
            DependenceEdgeType.SAME_GENERATED_SUMMARY: 0.85,
            DependenceEdgeType.SAME_THREAD: 0.55,
            DependenceEdgeType.SAME_TICKET: 0.50,
            DependenceEdgeType.SAME_AUTHOR_SAME_EVENT: 0.65,
        }
    )
    """Per-edge-type ceilings on δ. The realized δᵢⱼ for an edge of type t with
    weight w is ``edge_type_strength[t] * w``."""

    minimum_weight_floor: float = 0.05
    """We do not let any document's per-document weight fall below this. A
    document discovered through retrieval has at minimum some prior on
    contributing information; we never treat it as zero."""

    saturation: str = "logarithmic"
    """One of ``"linear"``, ``"logarithmic"``. Logarithmic saturation prevents a
    thousand mirrors of a single source from overwhelming a small number of
    independent sources. This is the recommended default."""


@dataclass(frozen=True)
class CorroborationResult:
    """Output of :func:`compute_effective_corroboration`."""

    effective_n: float
    """The C_eff value: an effective independent-source count."""

    per_document_weight: dict[str, float]
    """Per-document final weight in [0, 1]."""

    incoming_edges_by_doc: dict[str, list[DependenceEdge]]
    """Map from document id to the edges where it is the dependent."""


def _saturate(x: float, mode: str) -> float:
    """Apply saturation to a non-negative quantity ``x`` (lossy compression)."""
    if mode == "linear":
        return x
    if mode == "logarithmic":
        # 1 -> 1, 2 -> ~1.69, 5 -> ~2.79, 10 -> ~3.40, 100 -> ~5.62.
        # log1p of x. Smooth, monotonic, concave.
        return math.log1p(x)
    raise ValueError(f"Unknown saturation mode: {mode!r}")


def _strongest_edge_per_pair(
    edges: list[DependenceEdge],
) -> dict[tuple[str, str], DependenceEdge]:
    """Collapse multiple edges between the same ordered pair to the strongest."""
    by_pair: dict[tuple[str, str], DependenceEdge] = {}
    for e in edges:
        key = (e.source_id, e.target_id)
        existing = by_pair.get(key)
        if existing is None or e.weight > existing.weight:
            by_pair[key] = e
    return by_pair


def compute_effective_corroboration(
    documents: list[Document],
    edges: list[DependenceEdge],
    config: EffectiveCorroborationConfig | None = None,
) -> CorroborationResult:
    """Compute C_eff and per-document weights from documents and dependence edges.

    Algorithm
    ---------
    1. Each document starts with a per-source utility ``uᵢ`` derived from its
       upstream retrieval score (if provided) or 1.0.
    2. For each ordered (source, target) edge, we compute a per-edge delta
       ``δ = type_strength[type] * weight``, then attribute the discount to the
       *source* (the dependent) of the edge — this is the document we want to
       discount, since it is derivative.
    3. Each document's discount is the *maximum* δ across its incoming edges
       (we do not naively sum δ across types because they correlate).
    4. Per-document weight is ``max(uᵢ - discount, minimum_weight_floor)``.
    5. C_eff is the saturated sum of weights.

    Notes
    -----
    Step 3 (max instead of sum) prevents double-counting the discount itself
    when multiple typed-edge classifiers fire on the same pair. This is the
    "saturation" component of the V12 §4.6 δ_ij definition.
    """
    cfg = config or EffectiveCorroborationConfig()

    by_pair = _strongest_edge_per_pair(edges)

    # Per-document utility.
    utilities: dict[str, float] = {}
    for doc in documents:
        if doc.score is not None and 0.0 <= doc.score <= 1.0:
            utilities[doc.id] = doc.score
        else:
            utilities[doc.id] = 1.0

    # Per-document max discount and incoming edge list.
    per_doc_discount: dict[str, float] = {d.id: 0.0 for d in documents}
    per_doc_incoming: dict[str, list[DependenceEdge]] = {d.id: [] for d in documents}
    for (source_id, _target_id), edge in by_pair.items():
        type_strength = cfg.edge_type_strength.get(edge.edge_type, 0.5)
        delta = type_strength * edge.weight
        per_doc_incoming.setdefault(source_id, []).append(edge)
        if delta > per_doc_discount.get(source_id, 0.0):
            per_doc_discount[source_id] = delta

    # Per-document weight after discount.
    per_doc_weight: dict[str, float] = {}
    for doc in documents:
        u = utilities[doc.id]
        d = per_doc_discount.get(doc.id, 0.0)
        per_doc_weight[doc.id] = max(cfg.minimum_weight_floor, min(1.0, u - d))

    # C_eff: saturated sum of weights.
    raw_sum = sum(per_doc_weight.values())
    effective_n = _saturate(raw_sum, cfg.saturation)

    # If saturation produced something larger than naive count (logarithmic
    # cannot, but linear with all-ones could), clamp to naive count.
    effective_n = min(effective_n, float(len(documents)))

    return CorroborationResult(
        effective_n=effective_n,
        per_document_weight=per_doc_weight,
        incoming_edges_by_doc=per_doc_incoming,
    )


def topological_order(documents: list[Document], edges: list[DependenceEdge]) -> list[str]:
    """Return document IDs in topological order (sources before dependents).

    Useful for downstream tools that want to walk the DAG. If the graph cannot
    be ordered (which should not happen given the builder's cycle-breaking),
    falls back to lexicographic ID order.
    """
    graph: nx.DiGraph = nx.DiGraph()
    for d in documents:
        graph.add_node(d.id)
    for e in edges:
        # Source depends on target -> target should come first.
        graph.add_edge(e.target_id, e.source_id)
    try:
        return cast(list[str], list(nx.topological_sort(graph)))
    except nx.NetworkXUnfeasible:  # pragma: no cover — guarded upstream.
        return sorted(d.id for d in documents)
