"""Tests for the argus-rerank CLI."""

from __future__ import annotations

import json
from pathlib import Path

from argus_rerank.cli import main


def _write_docs(tmp_path: Path) -> Path:
    docs = [
        {"id": "a", "text": "The fox jumped over the lazy dog at noon."},
        {"id": "b", "text": "The fox jumped over the lazy dog at noon."},
        {"id": "c", "text": "An entirely different statement about chemistry."},
    ]
    p = tmp_path / "docs.json"
    p.write_text(json.dumps(docs), encoding="utf-8")
    return p


def test_cli_rerank_writes_json_output(tmp_path, capsys) -> None:  # type: ignore[no-untyped-def]
    docs_path = _write_docs(tmp_path)
    out_path = tmp_path / "out.json"

    rc = main(
        [
            "rerank",
            "--query",
            "What did the fox do?",
            "--documents",
            str(docs_path),
            "--output",
            str(out_path),
        ]
    )
    assert rc == 0
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert "ranked_documents" in payload
    assert payload["naive_count"] == 3


def test_cli_rerank_explain_to_stdout(tmp_path, capsys) -> None:  # type: ignore[no-untyped-def]
    docs_path = _write_docs(tmp_path)
    rc = main(
        [
            "rerank",
            "--query",
            "What did the fox do?",
            "--documents",
            str(docs_path),
            "--explain",
        ]
    )
    assert rc == 0
    captured = capsys.readouterr()
    assert "Effective independent sources" in captured.out
