"""Shared fixtures for ARGUS-Rerank tests."""

from __future__ import annotations

import pytest

from argus_rerank import Document


@pytest.fixture
def basic_documents() -> list[Document]:
    """Three documents with a clear independent / mirror / paraphrase structure."""
    return [
        Document(
            id="independent",
            text="The fox jumped over the lazy dog at noon on Tuesday.",
            source="A",
            author="alice",
            timestamp="2026-01-01T12:00:00",
        ),
        Document(
            id="mirror",
            text="The fox jumped over the lazy dog at noon on Tuesday.",
            source="B",
            author="bob",
            timestamp="2026-01-01T13:00:00",
        ),
        Document(
            id="paraphrase",
            text="At noon on Tuesday, an agile fox cleared the lazy hound.",
            source="C",
            author="carol",
            timestamp="2026-01-01T14:00:00",
        ),
    ]


@pytest.fixture
def thread_documents() -> list[Document]:
    """Two documents in the same thread, plus an outsider."""
    return [
        Document(
            id="t1",
            text="We need to ship this on Friday.",
            source="email",
            author="alice",
            timestamp="2026-02-01T09:00:00",
            thread_id="thread-42",
        ),
        Document(
            id="t2",
            text="Agreed — Friday it is. I'll prepare the release notes.",
            source="email",
            author="bob",
            timestamp="2026-02-01T09:30:00",
            thread_id="thread-42",
        ),
        Document(
            id="o1",
            text="Operations team is unaware of the Friday plan.",
            source="report",
            author="carol",
            timestamp="2026-02-02T08:00:00",
        ),
    ]
