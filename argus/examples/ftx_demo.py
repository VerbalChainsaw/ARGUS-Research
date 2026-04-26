"""End-to-end demo: dependence-aware corroboration on a synthetic FTX-like example.

Reproduces the README's "47 documents, 3 truly independent sources" intuition
on a small synthetic set. No external network calls.

Run::

    python examples/ftx_demo.py
"""

from __future__ import annotations

from argus_rerank import DependenceAwareReranker, Document


def build_demo_documents() -> list[Document]:
    """Build a synthetic FTX-like candidate set with intentional dependence patterns.

    The set contains:
      - Two genuinely independent eyewitness/forensic sources (d1, d4)
      - Two news mirrors of d1 (d2, d3) — a typical "echo chamber" pattern
      - One paraphrased quote of d1 with explicit attribution (d5)
      - One LLM-generated summary derived from d1 and d2 (d6)
    """
    return [
        Document(
            id="d1",
            text=(
                "FTX customer funds were not segregated from Alameda Research's "
                "trading accounts; investigators found commingled balances dating "
                "back to early 2022."
            ),
            source="WSJ",
            author="reporter_a",
            timestamp="2022-11-09T08:00:00",
        ),
        Document(
            id="d2",
            text=(
                "FTX customer funds were not segregated from Alameda Research's "
                "trading accounts. Investigators found commingled balances dating "
                "back to early 2022."
            ),
            source="Bloomberg",
            author="aggregator_b",
            timestamp="2022-11-09T11:30:00",
        ),
        Document(
            id="d3",
            text=(
                "FTX customer funds were not segregated from Alameda Research, "
                "according to investigators who found commingled balances dating "
                "back to early 2022."
            ),
            source="Reuters",
            author="aggregator_c",
            timestamp="2022-11-09T14:00:00",
        ),
        Document(
            id="d4",
            text=(
                "An internal Alameda memo dated April 2022 directs traders to draw "
                "on customer USDC pools to meet margin calls without notifying "
                "FTX users."
            ),
            source="court_filing",
            author="trustee",
            timestamp="2022-12-15",
        ),
        Document(
            id="d5",
            text=(
                "Per the WSJ report, FTX customer funds were not segregated from "
                "Alameda Research's trading accounts; the firm denies wrongdoing."
            ),
            source="business_journal",
            author="reporter_d",
            timestamp="2022-11-10",
            citations=["d1"],
        ),
        Document(
            id="d6",
            text=(
                "Multiple outlets report that FTX customer funds were commingled "
                "with Alameda accounts, with investigators citing balances dating "
                "back to early 2022 and a denial from FTX."
            ),
            source="ai_summary_service",
            author="ai-summarizer-v3",
            timestamp="2022-11-11",
            citations=["d1", "d2"],
            is_generated=True,
        ),
    ]


def main() -> None:
    documents = build_demo_documents()
    reranker = DependenceAwareReranker()
    result = reranker.rerank(
        query="Were FTX customer funds segregated from Alameda?",
        documents=documents,
    )

    print(result.explain())

    print("\n--- Ablation: dependence penalty disabled ---")
    from argus_rerank.reranker import RerankerConfig

    ablated = DependenceAwareReranker(
        config=RerankerConfig(enable_dependence_penalty=False)
    )
    ablated_result = ablated.rerank(
        query="Were FTX customer funds segregated from Alameda?",
        documents=documents,
    )
    print(ablated_result.explain())

    print()
    print("Effective independent source count:")
    print(f"  with    dependence penalty: {result.effective_n:.2f}")
    print(f"  without dependence penalty: {ablated_result.effective_n:.2f}")
    print(
        "Calibrated confidence:        "
        f"with={result.confidence:.2f}  without={ablated_result.confidence:.2f}"
    )


if __name__ == "__main__":
    main()
