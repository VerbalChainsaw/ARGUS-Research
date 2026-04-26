"""Construction of the typed dependence DAG over a candidate document set.

Combines surface signals (near-duplicate detection, copy-language detection)
with metadata signals (shared author/event, shared thread, shared ticket,
explicit citation, generated-summary marker) to produce typed dependence
edges per the ARGUS Codex §3.6 / V12 §10 taxonomy.

Resolves multiple inferred edges between the same ordered pair by keeping
the strongest one. The result is a DAG when timestamps are present (we
direct edges by time); when timestamps are missing we fall back to a stable
ID ordering, which keeps the structure acyclic but with weaker semantics.

Statement-class tags
--------------------
- :class:`DependenceGraphBuilder` — Architecture-conditional proposition.
  Edges are inferred under the assumption that surface and metadata signals
  approximate true source dependence. Failure cases are documented in
  ``docs/codex/03_defects.md`` D-NEW-1.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import cast

import networkx as nx

from argus_rerank.copy_detection import (
    CopyDetectionConfig,
    copy_signal_strength,
)
from argus_rerank.models import DependenceEdge, DependenceEdgeType, Document
from argus_rerank.near_duplicate import (
    MinHashConfig,
    MinHashLSHIndex,
    SimHashConfig,
    SimHasher,
)


@dataclass(frozen=True)
class DependenceGraphConfig:
    """Configuration knobs for dependence-graph construction."""

    simhash: SimHashConfig = field(default_factory=SimHashConfig)
    minhash: MinHashConfig = field(default_factory=MinHashConfig)
    copy: CopyDetectionConfig = field(default_factory=CopyDetectionConfig)

    same_author_event_window_days: int = 3
    """Two documents by the same author within this window are tagged
    SAME_AUTHOR_SAME_EVENT."""

    near_duplicate_jaccard_floor: float = 0.65
    """Jaccard at or above this triggers a MIRRORS edge regardless of SimHash."""


# --- Helpers ---------------------------------------------------------------


def _direction(a: Document, b: Document) -> tuple[Document, Document]:
    """Return ``(earlier, later)``. Later document depends on earlier.

    Falls back to ID lexicographic ordering when timestamps are missing or
    unparseable, which keeps the resulting graph acyclic but loses temporal
    semantics.
    """
    ta = _coerce_to_datetime(a.timestamp)
    tb = _coerce_to_datetime(b.timestamp)

    if ta is not None and tb is not None and ta != tb:
        return (a, b) if ta < tb else (b, a)
    return (a, b) if a.id < b.id else (b, a)


def _coerce_to_datetime(v: datetime | date | str | None) -> datetime | None:
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    if isinstance(v, date):
        return datetime(v.year, v.month, v.day)
    if isinstance(v, str):
        try:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def _days_apart(a: Document, b: Document) -> float | None:
    ta = _coerce_to_datetime(a.timestamp)
    tb = _coerce_to_datetime(b.timestamp)
    if ta is None or tb is None:
        return None
    return abs((ta - tb).total_seconds()) / 86400.0


# --- Builder ---------------------------------------------------------------


class DependenceGraphBuilder:
    """Construct typed dependence edges for a set of documents."""

    def __init__(self, config: DependenceGraphConfig | None = None) -> None:
        self.config = config or DependenceGraphConfig()
        self._simhasher = SimHasher(self.config.simhash)

    def build(self, documents: list[Document]) -> tuple[list[DependenceEdge], nx.DiGraph]:
        """Return ``(edges, dag)`` for the given document list."""
        if len(documents) < 2:
            graph: nx.DiGraph = nx.DiGraph()
            for d in documents:
                graph.add_node(d.id)
            return [], graph

        candidate_pairs = self._candidate_pairs(documents)

        edges_by_pair: dict[tuple[str, str], DependenceEdge] = {}

        for a, b in candidate_pairs:
            for inferred in self._infer_edges(a, b):
                key = (inferred.source_id, inferred.target_id)
                existing = edges_by_pair.get(key)
                if existing is None or inferred.weight > existing.weight:
                    edges_by_pair[key] = inferred

        edges = list(edges_by_pair.values())

        graph = nx.DiGraph()
        for d in documents:
            graph.add_node(d.id, document=d)
        for e in edges:
            graph.add_edge(
                e.source_id,
                e.target_id,
                edge_type=e.edge_type.value,
                weight=e.weight,
                evidence=e.evidence,
            )

        # If by chance timestamps produced a cycle (equal timestamps cycling
        # via ID fallback), break the smallest-weight edge until acyclic.
        # In practice this is rare; we keep the safety net cheap.
        while not nx.is_directed_acyclic_graph(graph):
            cycle = next(iter(nx.simple_cycles(graph)))
            cycle_edges = [
                (cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))
            ]
            weakest = min(
                cycle_edges,
                key=lambda uv: cast(float, graph.edges[uv]["weight"]),
            )
            graph.remove_edge(*weakest)
            edges = [
                e for e in edges
                if (e.source_id, e.target_id) != weakest
            ]

        return edges, graph

    # ----- Candidate pair generation ---------------------------------------

    def _candidate_pairs(
        self, documents: list[Document]
    ) -> Iterable[tuple[Document, Document]]:
        """Yield document pairs worth examining.

        For small candidate sets we examine all pairs; for larger sets we use
        MinHashLSH to filter to plausibly-similar pairs and merge in any pairs
        that share metadata signals (author+window, thread, ticket, citation).
        """
        n = len(documents)
        if n <= 50:
            for i in range(n):
                for j in range(i + 1, n):
                    yield documents[i], documents[j]
            return

        # Larger sets: LSH-filtered + metadata-anchored union.
        index = MinHashLSHIndex(self.config.minhash)
        for d in documents:
            index.insert(d.id, d.text)

        by_id = {d.id: d for d in documents}
        seen: set[tuple[str, str]] = set()

        # Surface-similar pairs from LSH.
        for a_id, b_id, _ in index.all_candidate_pairs():
            key = (a_id, b_id) if a_id < b_id else (b_id, a_id)
            if key in seen:
                continue
            seen.add(key)
            yield by_id[key[0]], by_id[key[1]]

        # Metadata-anchored pairs the surface signal might miss.
        for i in range(n):
            for j in range(i + 1, n):
                a, b = documents[i], documents[j]
                if not self._shares_metadata(a, b):
                    continue
                key = (a.id, b.id) if a.id < b.id else (b.id, a.id)
                if key in seen:
                    continue
                seen.add(key)
                yield by_id[key[0]], by_id[key[1]]

    def _shares_metadata(self, a: Document, b: Document) -> bool:
        if a.thread_id and a.thread_id == b.thread_id:
            return True
        if a.ticket_id and a.ticket_id == b.ticket_id:
            return True
        if a.id in b.citations or b.id in a.citations:
            return True
        if a.author and b.author and a.author == b.author:
            days = _days_apart(a, b)
            if days is not None and days <= self.config.same_author_event_window_days:
                return True
        return False

    # ----- Edge inference --------------------------------------------------

    def _infer_edges(self, a: Document, b: Document) -> list[DependenceEdge]:
        """Infer all applicable typed edges between two documents.

        Returns at most one edge per (source, target, type) tuple. The reranker
        de-duplicates further down to one edge per ordered pair (strongest
        wins).
        """
        edges: list[DependenceEdge] = []
        earlier, later = _direction(a, b)

        # Surface similarity: SimHash + Jaccard.
        sim = self._simhasher.similarity(a.text, b.text)
        copy = copy_signal_strength(a.text, b.text, self.config.copy)
        is_simhash_near_duplicate = self._simhasher.is_near_duplicate(a.text, b.text)
        is_high_jaccard = copy.ngram_jaccard >= self.config.near_duplicate_jaccard_floor

        if is_simhash_near_duplicate or is_high_jaccard:
            mirror_weight = max(sim, copy.strength)
            edges.append(
                DependenceEdge(
                    source_id=later.id,
                    target_id=earlier.id,
                    edge_type=DependenceEdgeType.MIRRORS,
                    weight=min(1.0, mirror_weight),
                    evidence=(
                        f"simhash_sim={sim:.2f} jaccard={copy.ngram_jaccard:.2f}"
                    ),
                )
            )
        elif copy.ngram_jaccard >= self.config.copy.jaccard_quote_threshold or (
            copy.longest_common_run >= self.config.copy.min_span_for_quote
        ):
            quote_weight = copy.strength
            edges.append(
                DependenceEdge(
                    source_id=later.id,
                    target_id=earlier.id,
                    edge_type=DependenceEdgeType.QUOTE_OF,
                    weight=min(1.0, quote_weight),
                    evidence=(
                        f"jaccard={copy.ngram_jaccard:.2f} "
                        f"common_run={copy.longest_common_run}"
                    ),
                )
            )

        # Explicit citation -> DERIVED_FROM (stronger semantics than QUOTE_OF).
        if earlier.id in later.citations:
            edges.append(
                DependenceEdge(
                    source_id=later.id,
                    target_id=earlier.id,
                    edge_type=DependenceEdgeType.DERIVED_FROM,
                    weight=0.85,
                    evidence="explicit citation in document.citations",
                )
            )

        # Generated summary heuristic.
        if later.is_generated and earlier.is_generated and copy.strength >= 0.3:
            edges.append(
                DependenceEdge(
                    source_id=later.id,
                    target_id=earlier.id,
                    edge_type=DependenceEdgeType.SAME_GENERATED_SUMMARY,
                    weight=min(1.0, 0.5 + copy.strength * 0.5),
                    evidence="both flagged is_generated with copy signal",
                )
            )
        elif later.is_generated and earlier.id in later.citations:
            edges.append(
                DependenceEdge(
                    source_id=later.id,
                    target_id=earlier.id,
                    edge_type=DependenceEdgeType.SUMMARY_OF,
                    weight=0.9,
                    evidence="generated document citing earlier as source",
                )
            )

        # Same thread / ticket are direct metadata signals.
        if a.thread_id and a.thread_id == b.thread_id:
            edges.append(
                DependenceEdge(
                    source_id=later.id,
                    target_id=earlier.id,
                    edge_type=DependenceEdgeType.SAME_THREAD,
                    weight=0.55,
                    evidence=f"thread_id={a.thread_id}",
                )
            )
        if a.ticket_id and a.ticket_id == b.ticket_id:
            edges.append(
                DependenceEdge(
                    source_id=later.id,
                    target_id=earlier.id,
                    edge_type=DependenceEdgeType.SAME_TICKET,
                    weight=0.5,
                    evidence=f"ticket_id={a.ticket_id}",
                )
            )

        # Same-author-same-event: same author, within configured window, similar topic.
        if a.author and b.author and a.author == b.author:
            days = _days_apart(a, b)
            within_window = (
                days is not None and days <= self.config.same_author_event_window_days
            )
            # Only emit if there's at least *some* topical overlap; otherwise an
            # author writing about two unrelated things is not dependence.
            has_topical_overlap = copy.strength >= 0.05 or sim >= 0.6
            if within_window and has_topical_overlap:
                edges.append(
                    DependenceEdge(
                        source_id=later.id,
                        target_id=earlier.id,
                        edge_type=DependenceEdgeType.SAME_AUTHOR_SAME_EVENT,
                        weight=min(0.7, 0.4 + copy.strength * 0.3),
                        evidence=(
                            f"same author '{a.author}', within "
                            f"{self.config.same_author_event_window_days} days"
                        ),
                    )
                )

        return edges
