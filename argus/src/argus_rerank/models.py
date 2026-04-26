"""Pydantic data models for ARGUS-Rerank (import package ``argus_rerank``).

These types are the public boundary of the library. They are deliberately
small: a :class:`Document` carries the metadata we need for dependence
inference (source, author, timestamp, optional thread/ticket identifiers),
and a :class:`RerankResult` carries the dependence graph and computed
quantities back to the caller.

The :class:`DependenceEdgeType` enum mirrors the V12 §10 typed-edge taxonomy
verbatim (see ``docs/codex/02_v12_canonical_definitions.md`` §3.6).

Statement-class tags
--------------------
- :class:`DependenceEdgeType` — Definition (matches V12 spec).
- :attr:`DependenceEdge.weight` — Engineering rule. The default weights are
  drawn from the ARGUS Codex §4 D-NEW-1 recommendation; they are not theorems.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DependenceEdgeType(str, Enum):
    """Typed dependence-edge taxonomy from ARGUS Codex §3.6 / V12 §10.

    Two documents A and B related by an edge of these types should have their
    naive corroboration count discounted; B is not an independent confirmation
    of A.
    """

    DERIVED_FROM = "derived-from"
    """B is generated/derived from A. Strong dependence."""

    MIRRORS = "mirrors"
    """A and B are near-textual duplicates. Strongest possible dependence."""

    SUMMARY_OF = "summary-of"
    """B is a summary of A. Strong dependence."""

    QUOTE_OF = "quote-of"
    """B explicitly quotes/attributes content from A. Moderate dependence."""

    SAME_AUTHOR_SAME_EVENT = "same-author-same-event"
    """A and B are different items by the same author about the same event."""

    SAME_THREAD = "same-thread"
    """A and B are part of the same conversation thread (email, chat, etc.)."""

    SAME_TICKET = "same-ticket"
    """A and B are tied to the same ticket/case identifier."""

    SAME_GENERATED_SUMMARY = "same-generated-summary"
    """A and B are both LLM-generated summaries of overlapping evidence."""


class Document(BaseModel):
    """A retrieved document candidate.

    Only :attr:`id` and :attr:`text` are required. Every other field is metadata
    used by dependence inference; missing metadata simply weakens the signals
    available to the reranker (it does not crash).

    Notes
    -----
    The reranker is robust to missing metadata: if no timestamps or authors are
    provided, dependence inference falls back on textual similarity alone. This
    is by design — many corpora are messier than ideal.
    """

    model_config = ConfigDict(extra="allow", frozen=False)

    id: str = Field(..., description="Stable identifier for this document.")
    text: str = Field(..., description="The textual content used for similarity.")
    source: str | None = Field(
        default=None,
        description="Origin (publisher, system, repo, mailbox). Used for source-type "
        "separation in the dependence graph.",
    )
    author: str | None = Field(default=None, description="Author/agent identifier.")
    timestamp: datetime | date | str | None = Field(
        default=None,
        description="When the document was created. Accepts ISO strings; they are "
        "normalized to :class:`datetime` when possible.",
    )
    thread_id: str | None = Field(
        default=None,
        description="Optional thread/conversation identifier (e.g. email Message-ID "
        "thread root). Used for the SAME_THREAD edge type.",
    )
    ticket_id: str | None = Field(
        default=None,
        description="Optional case/ticket identifier. Used for SAME_TICKET edges.",
    )
    citations: list[str] = Field(
        default_factory=list,
        description="Document IDs this document explicitly cites or quotes. Used "
        "for QUOTE_OF / DERIVED_FROM edge inference.",
    )
    is_generated: bool = Field(
        default=False,
        description="True if this document is known to be LLM-generated. Used for "
        "SAME_GENERATED_SUMMARY edge inference.",
    )
    score: float | None = Field(
        default=None,
        description="Optional upstream retrieval score (BM25, cosine, etc.). Treated "
        "as a soft prior on initial weight.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Free-form metadata bag for downstream consumers. Not used by "
        "the reranker.",
    )

    @field_validator("text")
    @classmethod
    def _text_nonempty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Document.text must be non-empty after stripping whitespace.")
        return v

    @field_validator("timestamp", mode="before")
    @classmethod
    def _normalize_timestamp(cls, v: Any) -> Any:
        if v is None or isinstance(v, (datetime, date)):
            return v
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                return v
        return v


class DependenceEdge(BaseModel):
    """A typed dependence relation between two documents.

    The :attr:`weight` is in [0, 1]: 1.0 means "fully derivative, contributes
    no independent information" and 0.0 means "no detected dependence".

    Engineering rule (Codex §4 D-NEW-1): δᵢⱼ in the C_eff formula is computed
    by saturating the maximum-weighted edge between i and j (we do not naively
    sum overlapping evidence of dependence; that would double-count the
    discount itself).
    """

    model_config = ConfigDict(extra="forbid", frozen=False)

    source_id: str = Field(..., description="ID of the document that is the dependent (B).")
    target_id: str = Field(..., description="ID of the document being depended upon (A).")
    edge_type: DependenceEdgeType
    weight: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Strength of dependence in [0, 1]. 1.0 = fully derivative.",
    )
    evidence: str | None = Field(
        default=None,
        description="Optional human-readable explanation of why this edge was inferred.",
    )

    @field_validator("source_id", "target_id")
    @classmethod
    def _ids_nonempty(cls, v: str) -> str:
        if not v:
            raise ValueError("Edge endpoint IDs must be non-empty.")
        return v


class RankedDocument(BaseModel):
    """A document together with its computed weight and dependence summary."""

    model_config = ConfigDict(extra="forbid")

    document: Document
    weight: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Final per-document weight in [0, 1] after dependence discounting.",
    )
    dependence_summary: str = Field(
        ...,
        description="One-line human-readable summary of why this weight was assigned.",
    )
    incoming_edges: list[DependenceEdge] = Field(
        default_factory=list,
        description="Edges where this document is the dependent (source_id).",
    )

    @property
    def is_independent(self) -> bool:
        """True if no significant incoming dependence edges exist."""
        return all(e.weight < 0.25 for e in self.incoming_edges)


class RerankResult(BaseModel):
    """Final output of :meth:`DependenceAwareReranker.rerank`.

    Notes
    -----
    :attr:`confidence` is an empirical, calibrated estimator — *not* a Bayesian
    posterior. See ARGUS Codex §3.1 (Claim Support Field) and §3.9 (Calibration
    Law) for the precise statement-class.
    """

    model_config = ConfigDict(extra="forbid")

    query: str
    naive_count: int = Field(
        ...,
        description="Number of input documents (before dependence discounting).",
    )
    effective_n: float = Field(
        ...,
        ge=0.0,
        description="Effective independent-source count C_eff.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Calibrated confidence in [0, 1] for the underlying claim.",
    )
    ranked_documents: list[RankedDocument] = Field(
        ...,
        description="Documents in descending weight order.",
    )
    dependence_edges: list[DependenceEdge] = Field(
        default_factory=list,
        description="All inferred dependence edges (the dependence DAG).",
    )

    def explain(self) -> str:
        """Return a human-readable explanation of the reranking decision."""
        lines = [
            f"Query: {self.query}",
            f"Naive corroboration count:        {self.naive_count}",
            f"Effective independent sources:    {self.effective_n:.2f}",
            f"Calibrated claim confidence:      {self.confidence:.2f}",
            "",
            "Ranked documents:",
        ]
        for rd in self.ranked_documents:
            lines.append(
                f"  {rd.document.id:>6}  weight={rd.weight:.2f}  "
                f"reason={rd.dependence_summary}"
            )
        if self.dependence_edges:
            lines.append("")
            lines.append("Dependence edges:")
            for e in self.dependence_edges:
                lines.append(
                    f"  {e.source_id} --{e.edge_type.value} (w={e.weight:.2f})--> {e.target_id}"
                )
        return "\n".join(lines)
