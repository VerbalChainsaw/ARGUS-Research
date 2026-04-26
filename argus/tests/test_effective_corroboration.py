"""Tests for effective corroboration computation."""

from __future__ import annotations

import math

from argus_rerank import Document
from argus_rerank.effective_corroboration import (
    EffectiveCorroborationConfig,
    compute_effective_corroboration,
    topological_order,
)
from argus_rerank.models import DependenceEdge, DependenceEdgeType


class TestComputeEffectiveCorroboration:
    def test_no_edges_no_discount(self) -> None:
        docs = [Document(id=f"d{i}", text=f"text {i}") for i in range(3)]
        result = compute_effective_corroboration(docs, edges=[])
        # Logarithmic saturation: log1p(3) ~= 1.386
        assert math.isclose(result.effective_n, math.log1p(3.0), rel_tol=1e-6)
        assert all(w == 1.0 for w in result.per_document_weight.values())

    def test_full_mirror_discounts_one_source(self) -> None:
        docs = [Document(id="a", text="t"), Document(id="b", text="t")]
        edges = [
            DependenceEdge(
                source_id="b",
                target_id="a",
                edge_type=DependenceEdgeType.MIRRORS,
                weight=1.0,
            )
        ]
        result = compute_effective_corroboration(docs, edges)
        # b should be heavily discounted; a should retain weight 1.0
        assert result.per_document_weight["a"] == 1.0
        assert result.per_document_weight["b"] < 0.2

    def test_minimum_weight_floor_applied(self) -> None:
        docs = [Document(id="a", text="t"), Document(id="b", text="t")]
        edges = [
            DependenceEdge(
                source_id="b",
                target_id="a",
                edge_type=DependenceEdgeType.MIRRORS,
                weight=1.0,
            )
        ]
        cfg = EffectiveCorroborationConfig(minimum_weight_floor=0.1)
        result = compute_effective_corroboration(docs, edges, cfg)
        assert result.per_document_weight["b"] >= 0.1

    def test_strongest_edge_per_pair_used(self) -> None:
        """If two edges link the same ordered pair, the stronger is what discounts."""
        docs = [Document(id="a", text="t"), Document(id="b", text="t")]
        edges = [
            DependenceEdge(
                source_id="b",
                target_id="a",
                edge_type=DependenceEdgeType.QUOTE_OF,
                weight=0.4,
            ),
            DependenceEdge(
                source_id="b",
                target_id="a",
                edge_type=DependenceEdgeType.MIRRORS,
                weight=0.95,
            ),
        ]
        result = compute_effective_corroboration(docs, edges)
        # b's discount should be governed by the MIRRORS edge (stronger).
        weight_only_quote = compute_effective_corroboration(
            docs, edges=[edges[0]]
        ).per_document_weight["b"]
        assert result.per_document_weight["b"] < weight_only_quote

    def test_logarithmic_saturation(self) -> None:
        """A thousand mirrors of one source should not give 1000x effective n."""
        docs = [Document(id=f"d{i}", text="same text") for i in range(100)]
        edges = []
        for i in range(1, 100):
            edges.append(
                DependenceEdge(
                    source_id=f"d{i}",
                    target_id="d0",
                    edge_type=DependenceEdgeType.MIRRORS,
                    weight=1.0,
                )
            )
        result = compute_effective_corroboration(docs, edges)
        # All but d0 should be at the floor, so raw_sum is approx 1 + 99*0.05 = 5.95
        # log1p(5.95) ~= 1.94
        assert result.effective_n < 3.0

    def test_three_independent_sources_realistic_count(self) -> None:
        docs = [Document(id=f"d{i}", text=f"text {i}") for i in range(3)]
        result = compute_effective_corroboration(docs, edges=[])
        # log1p(3.0) ~= 1.386
        assert 1.3 < result.effective_n < 1.5

    def test_score_used_as_utility_when_provided(self) -> None:
        docs = [Document(id="a", text="t", score=0.5)]
        result = compute_effective_corroboration(docs, edges=[])
        assert result.per_document_weight["a"] == 0.5

    def test_effective_n_capped_at_naive_count(self) -> None:
        docs = [Document(id=f"d{i}", text=f"t{i}") for i in range(2)]
        cfg = EffectiveCorroborationConfig(saturation="linear")
        result = compute_effective_corroboration(docs, edges=[], config=cfg)
        assert result.effective_n <= 2.0


class TestTopologicalOrder:
    def test_orders_targets_before_sources(self) -> None:
        docs = [
            Document(id="a", text="text a"),
            Document(id="b", text="text b"),
            Document(id="c", text="text c"),
        ]
        edges = [
            DependenceEdge(
                source_id="b",
                target_id="a",
                edge_type=DependenceEdgeType.QUOTE_OF,
                weight=0.5,
            ),
            DependenceEdge(
                source_id="c",
                target_id="b",
                edge_type=DependenceEdgeType.QUOTE_OF,
                weight=0.5,
            ),
        ]
        order = topological_order(docs, edges)
        assert order.index("a") < order.index("b") < order.index("c")
