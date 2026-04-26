"""Tests for Pydantic data models."""

from __future__ import annotations

from datetime import datetime

import pytest

from argus_rerank import (
    DependenceEdge,
    DependenceEdgeType,
    Document,
    RankedDocument,
    RerankResult,
)


class TestDocument:
    def test_minimum_required_fields(self) -> None:
        d = Document(id="a", text="hello world")
        assert d.id == "a"
        assert d.text == "hello world"
        assert d.source is None
        assert d.citations == []

    def test_iso_timestamp_normalized(self) -> None:
        d = Document(id="a", text="hi", timestamp="2026-04-26T12:30:00Z")
        assert isinstance(d.timestamp, datetime)
        assert d.timestamp.year == 2026

    def test_unparseable_timestamp_kept_as_string(self) -> None:
        d = Document(id="a", text="hi", timestamp="last Tuesday")
        assert d.timestamp == "last Tuesday"

    def test_empty_text_rejected(self) -> None:
        with pytest.raises(ValueError):
            Document(id="a", text="   ")

    def test_extra_fields_allowed(self) -> None:
        d = Document(id="a", text="hi", weird_field=42)  # type: ignore[call-arg]
        assert getattr(d, "weird_field", None) == 42


class TestDependenceEdge:
    def test_valid(self) -> None:
        e = DependenceEdge(
            source_id="b",
            target_id="a",
            edge_type=DependenceEdgeType.MIRRORS,
            weight=0.9,
        )
        assert e.weight == 0.9

    def test_weight_must_be_in_range(self) -> None:
        with pytest.raises(ValueError):
            DependenceEdge(
                source_id="b",
                target_id="a",
                edge_type=DependenceEdgeType.MIRRORS,
                weight=1.5,
            )

    def test_ids_must_be_nonempty(self) -> None:
        with pytest.raises(ValueError):
            DependenceEdge(
                source_id="",
                target_id="a",
                edge_type=DependenceEdgeType.MIRRORS,
                weight=0.5,
            )


class TestEdgeTaxonomy:
    def test_all_codex_edges_present(self) -> None:
        """V12 §10 enumerates exactly 8 typed dependence edges. We must implement them all."""
        expected = {
            "derived-from",
            "mirrors",
            "summary-of",
            "quote-of",
            "same-author-same-event",
            "same-thread",
            "same-ticket",
            "same-generated-summary",
        }
        actual = {e.value for e in DependenceEdgeType}
        assert actual == expected


class TestRankedDocument:
    def test_independence_property(self) -> None:
        doc = Document(id="a", text="text")
        rd = RankedDocument(
            document=doc,
            weight=0.9,
            dependence_summary="independent",
            incoming_edges=[],
        )
        assert rd.is_independent

        rd2 = RankedDocument(
            document=doc,
            weight=0.3,
            dependence_summary="mirrors",
            incoming_edges=[
                DependenceEdge(
                    source_id="a",
                    target_id="b",
                    edge_type=DependenceEdgeType.MIRRORS,
                    weight=0.9,
                )
            ],
        )
        assert not rd2.is_independent


class TestRerankResult:
    def test_explain_contains_key_fields(self) -> None:
        result = RerankResult(
            query="Q",
            naive_count=2,
            effective_n=1.5,
            confidence=0.7,
            ranked_documents=[
                RankedDocument(
                    document=Document(id="a", text="t"),
                    weight=1.0,
                    dependence_summary="independent",
                )
            ],
            dependence_edges=[],
        )
        explanation = result.explain()
        assert "Q" in explanation
        assert "1.50" in explanation
        assert "0.70" in explanation
