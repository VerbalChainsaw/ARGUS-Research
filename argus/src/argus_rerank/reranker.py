"""Top-level :class:`DependenceAwareReranker` API.

Orchestrates the four stages:
    1. Build the typed dependence DAG.
    2. Compute effective corroboration C_eff and per-document weights.
    3. Calibrate the resulting support summary into a claim confidence in [0,1].
    4. Emit a :class:`RerankResult` with ranked documents in descending weight.

Statement-class
---------------
- The orchestration is an Engineering rule. The end-to-end behavior is a
  composition of pieces whose individual classes are documented in their
  respective modules.
- Falsifiability statement (ARGUS Codex W-3): if ablating the dependence
  penalty does not statistically degrade end-to-end accuracy on Stock /
  RAMDocs / FEVEROUS, the central claim of the wedge is refuted.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from argus_rerank.calibration import (
    CalibrationRegistry,
    SupportFeatures,
)
from argus_rerank.dependence_graph import (
    DependenceGraphBuilder,
    DependenceGraphConfig,
)
from argus_rerank.effective_corroboration import (
    EffectiveCorroborationConfig,
    compute_effective_corroboration,
)
from argus_rerank.models import (
    DependenceEdge,
    DependenceEdgeType,
    Document,
    RankedDocument,
    RerankResult,
)


@dataclass
class RerankerConfig:
    """Top-level reranker configuration. Each sub-config is optional."""

    graph: DependenceGraphConfig = field(default_factory=DependenceGraphConfig)
    corroboration: EffectiveCorroborationConfig = field(
        default_factory=EffectiveCorroborationConfig
    )
    independence_threshold: float = 0.25
    """Documents whose strongest incoming edge is below this threshold are
    counted as independent for calibration purposes."""

    enable_dependence_penalty: bool = True
    """Set to ``False`` to ablate the dependence-aware contribution. Useful
    for the dependence-penalty ablation per ARGUS Codex D-2026-05."""


class DependenceAwareReranker:
    """Reranks retrieved documents by discounting correlated evidence.

    Examples
    --------
    >>> from argus_rerank import DependenceAwareReranker, Document
    >>> reranker = DependenceAwareReranker()
    >>> docs = [
    ...     Document(id="a", text="The sky is blue."),
    ...     Document(id="b", text="The sky is blue."),
    ... ]
    >>> result = reranker.rerank(query="What color is the sky?", documents=docs)
    >>> 0.0 <= result.confidence <= 1.0
    True
    """

    def __init__(
        self,
        config: RerankerConfig | None = None,
        calibration: CalibrationRegistry | None = None,
    ) -> None:
        self.config = config or RerankerConfig()
        self.calibration = calibration or CalibrationRegistry()
        self._graph_builder = DependenceGraphBuilder(self.config.graph)

    def rerank(
        self,
        query: str,
        documents: list[Document],
        query_class: str = "default",
    ) -> RerankResult:
        """Rerank ``documents`` for ``query`` and return a calibrated result."""
        if not documents:
            return RerankResult(
                query=query,
                naive_count=0,
                effective_n=0.0,
                confidence=0.0,
                ranked_documents=[],
                dependence_edges=[],
            )

        # Stage 1: build the dependence DAG.
        if self.config.enable_dependence_penalty:
            edges, _graph = self._graph_builder.build(documents)
        else:
            edges = []

        # Stage 2: compute C_eff and per-document weights.
        corroboration = compute_effective_corroboration(
            documents,
            edges,
            self.config.corroboration,
        )

        # Stage 3: calibrate.
        n_independent = sum(
            1
            for d in documents
            if all(
                e.weight < self.config.independence_threshold
                for e in corroboration.incoming_edges_by_doc.get(d.id, [])
            )
        )
        features = SupportFeatures.from_per_document_weights(
            weights=corroboration.per_document_weight,
            effective_n=corroboration.effective_n,
            n_independent_documents=n_independent,
        )
        confidence = self.calibration.predict(features, query_class=query_class)

        # Stage 4: assemble ranked output.
        ranked = self._assemble_ranked_documents(
            documents,
            corroboration.per_document_weight,
            corroboration.incoming_edges_by_doc,
        )

        return RerankResult(
            query=query,
            naive_count=len(documents),
            effective_n=corroboration.effective_n,
            confidence=confidence,
            ranked_documents=ranked,
            dependence_edges=edges,
        )

    @staticmethod
    def _assemble_ranked_documents(
        documents: list[Document],
        per_doc_weight: dict[str, float],
        incoming_edges: dict[str, list[DependenceEdge]],
    ) -> list[RankedDocument]:
        ranked: list[RankedDocument] = []
        for d in documents:
            edges_in = incoming_edges.get(d.id, [])
            ranked.append(
                RankedDocument(
                    document=d,
                    weight=per_doc_weight.get(d.id, 0.0),
                    dependence_summary=_summarize_dependence(edges_in),
                    incoming_edges=edges_in,
                )
            )
        ranked.sort(key=lambda rd: rd.weight, reverse=True)
        return ranked


def _summarize_dependence(edges: list[DependenceEdge]) -> str:
    """One-line human-readable summary of why a document was discounted."""
    if not edges:
        return "independent"
    strongest = max(edges, key=lambda e: e.weight)
    return _phrase_for_edge(strongest)


def _phrase_for_edge(edge: DependenceEdge) -> str:
    base = {
        DependenceEdgeType.MIRRORS: f"mirrors {edge.target_id} (near-duplicate)",
        DependenceEdgeType.DERIVED_FROM: f"derived from {edge.target_id}",
        DependenceEdgeType.SUMMARY_OF: f"summary of {edge.target_id}",
        DependenceEdgeType.QUOTE_OF: f"quote-of {edge.target_id}",
        DependenceEdgeType.SAME_AUTHOR_SAME_EVENT: f"same author as {edge.target_id}, same event",
        DependenceEdgeType.SAME_THREAD: f"same thread as {edge.target_id}",
        DependenceEdgeType.SAME_TICKET: f"same ticket as {edge.target_id}",
        DependenceEdgeType.SAME_GENERATED_SUMMARY: f"co-generated with {edge.target_id}",
    }[edge.edge_type]
    return base
