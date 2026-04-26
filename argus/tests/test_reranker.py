"""Tests for the top-level DependenceAwareReranker."""

from __future__ import annotations

from argus_rerank import DependenceAwareReranker, Document, RerankResult
from argus_rerank.reranker import RerankerConfig


class TestDependenceAwareReranker:
    def test_empty_documents(self) -> None:
        reranker = DependenceAwareReranker()
        result = reranker.rerank(query="anything", documents=[])
        assert isinstance(result, RerankResult)
        assert result.naive_count == 0
        assert result.effective_n == 0.0
        assert result.confidence == 0.0
        assert result.ranked_documents == []

    def test_single_document(self) -> None:
        reranker = DependenceAwareReranker()
        result = reranker.rerank(
            query="anything",
            documents=[Document(id="a", text="some statement about something")],
        )
        assert result.naive_count == 1
        assert len(result.ranked_documents) == 1
        assert result.ranked_documents[0].dependence_summary == "independent"

    def test_independent_sources_outweigh_mirrors(self, basic_documents) -> None:  # type: ignore[no-untyped-def]
        reranker = DependenceAwareReranker()
        result = reranker.rerank(query="Q", documents=basic_documents)

        ids_in_order = [rd.document.id for rd in result.ranked_documents]
        # Mirror should rank below the original/independent.
        assert ids_in_order.index("mirror") > ids_in_order.index("independent")

    def test_dependence_penalty_reduces_effective_n(self, basic_documents) -> None:  # type: ignore[no-untyped-def]
        with_penalty = DependenceAwareReranker().rerank(
            query="Q", documents=basic_documents
        )
        without_penalty = DependenceAwareReranker(
            config=RerankerConfig(enable_dependence_penalty=False)
        ).rerank(query="Q", documents=basic_documents)

        assert with_penalty.effective_n <= without_penalty.effective_n
        # Confidence should also be no higher when we *remove* the penalty,
        # because raw count goes up but each source still contributes.
        # (Strict ordering not guaranteed because of saturation.)

    def test_thread_documents_get_dependence_edge(self, thread_documents) -> None:  # type: ignore[no-untyped-def]
        reranker = DependenceAwareReranker()
        result = reranker.rerank(query="Q", documents=thread_documents)
        edge_types = {e.edge_type.value for e in result.dependence_edges}
        assert "same-thread" in edge_types

    def test_explain_runs(self, basic_documents) -> None:  # type: ignore[no-untyped-def]
        result = DependenceAwareReranker().rerank(query="Q", documents=basic_documents)
        text = result.explain()
        assert "Query: Q" in text
        assert "Naive corroboration count" in text
        assert "Effective independent sources" in text

    def test_confidence_in_unit_interval(self, basic_documents) -> None:  # type: ignore[no-untyped-def]
        result = DependenceAwareReranker().rerank(query="Q", documents=basic_documents)
        assert 0.0 <= result.confidence <= 1.0


class TestFalsifiabilityScenario:
    """Sanity checks tied to the ARGUS Codex W-3 falsifiability statement.

    "If on a held-out evaluation, removing the dependence penalty does not
    statistically degrade Stock MAE or RAMDocs EM, the central claim is refuted."

    These are unit tests, not benchmarks; we only verify the *machinery*
    behaves as required so that the empirical claim is testable downstream.
    """

    def test_ablation_machinery_changes_effective_n(self) -> None:
        docs = [
            Document(
                id=f"d{i}",
                text="The same exact sentence repeated verbatim to be detected.",
                source=f"src-{i}",
                author=f"author-{i}",
                timestamp=f"2026-01-{i + 1:02d}",
            )
            for i in range(5)
        ]
        with_penalty = DependenceAwareReranker().rerank(query="Q", documents=docs)
        without_penalty = DependenceAwareReranker(
            config=RerankerConfig(enable_dependence_penalty=False)
        ).rerank(query="Q", documents=docs)

        # With dependence penalty on, 5 mirrors should collapse to ~ 1 effective source.
        assert with_penalty.effective_n < 2.0
        # Without it, all 5 contribute fully (saturated to log1p(5) ~ 1.79
        # given the default logarithmic saturation).
        assert without_penalty.effective_n > with_penalty.effective_n
