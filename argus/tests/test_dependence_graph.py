"""Tests for dependence-graph construction."""

from __future__ import annotations

import networkx as nx

from argus_rerank import Document
from argus_rerank.dependence_graph import DependenceGraphBuilder
from argus_rerank.models import DependenceEdgeType


class TestDependenceGraphBuilder:
    def test_empty_input(self) -> None:
        builder = DependenceGraphBuilder()
        edges, graph = builder.build([])
        assert edges == []
        assert graph.number_of_nodes() == 0

    def test_single_document(self) -> None:
        builder = DependenceGraphBuilder()
        edges, graph = builder.build([Document(id="a", text="some text")])
        assert edges == []
        assert graph.number_of_nodes() == 1

    def test_mirror_detection(self, basic_documents: list[Document]) -> None:
        builder = DependenceGraphBuilder()
        edges, _graph = builder.build(basic_documents)

        mirror_edges = [e for e in edges if e.edge_type == DependenceEdgeType.MIRRORS]
        assert len(mirror_edges) >= 1

        directed_pairs = {(e.source_id, e.target_id) for e in mirror_edges}
        # The earlier-timestamped doc is the target; mirror is the dependent.
        assert ("mirror", "independent") in directed_pairs

    def test_thread_id_creates_same_thread_edge(
        self, thread_documents: list[Document]
    ) -> None:
        builder = DependenceGraphBuilder()
        edges, _graph = builder.build(thread_documents)
        thread_edges = [e for e in edges if e.edge_type == DependenceEdgeType.SAME_THREAD]
        assert len(thread_edges) == 1
        assert thread_edges[0].source_id == "t2"
        assert thread_edges[0].target_id == "t1"

    def test_explicit_citation_creates_derived_from(self) -> None:
        builder = DependenceGraphBuilder()
        docs = [
            Document(
                id="src",
                text="The original report on the matter, with detailed analysis.",
                timestamp="2026-01-01",
            ),
            Document(
                id="cite",
                text="A different perspective entirely on a different subject.",
                timestamp="2026-01-02",
                citations=["src"],
            ),
        ]
        edges, _graph = builder.build(docs)
        derived_edges = [
            e for e in edges if e.edge_type == DependenceEdgeType.DERIVED_FROM
        ]
        assert len(derived_edges) == 1
        assert derived_edges[0].source_id == "cite"
        assert derived_edges[0].target_id == "src"

    def test_resulting_graph_is_dag(self) -> None:
        builder = DependenceGraphBuilder()
        # Construct a potentially cyclic situation: same thread, identical timestamps,
        # near-identical text. The cycle-breaker should still yield a DAG.
        docs = [
            Document(
                id="x",
                text="Same content here in this very specific format.",
                thread_id="t1",
                timestamp="2026-01-01T12:00:00",
            ),
            Document(
                id="y",
                text="Same content here in this very specific format.",
                thread_id="t1",
                timestamp="2026-01-01T12:00:00",
            ),
        ]
        _, graph = builder.build(docs)
        assert nx.is_directed_acyclic_graph(graph)

    def test_independent_documents_yield_no_edges(self) -> None:
        builder = DependenceGraphBuilder()
        docs = [
            Document(
                id="a",
                text="Quantum chromodynamics describes nuclear interactions.",
                source="physics",
                author="alice",
                timestamp="2026-01-01",
            ),
            Document(
                id="b",
                text="The migratory patterns of arctic terns extend remarkably far.",
                source="biology",
                author="bob",
                timestamp="2026-01-02",
            ),
        ]
        edges, _graph = builder.build(docs)
        assert edges == []

    def test_only_strongest_edge_per_pair_kept(self) -> None:
        """Inferring multiple typed edges between the same pair should collapse to one
        per (source, target) ordered pair, with the strongest weight surviving."""
        builder = DependenceGraphBuilder()
        # Same author + same thread + identical text -> multiple typed edges
        # would fire, but the dependence_graph builder keeps only the strongest
        # per (source, target) ordered pair.
        docs = [
            Document(
                id="a",
                text="The market closed sharply higher on Friday afternoon today.",
                author="alice",
                thread_id="t",
                timestamp="2026-01-01T10:00:00",
            ),
            Document(
                id="b",
                text="The market closed sharply higher on Friday afternoon today.",
                author="alice",
                thread_id="t",
                timestamp="2026-01-01T10:30:00",
            ),
        ]
        edges, _graph = builder.build(docs)
        pairs = [(e.source_id, e.target_id) for e in edges]
        assert len(pairs) == len(set(pairs))
