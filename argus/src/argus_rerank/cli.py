"""Minimal CLI for ARGUS-Rerank (import package ``argus_rerank``).

Usage::

    argus-rerank rerank --query "What color is the sky?" --documents docs.json

``docs.json`` is a JSON array of objects matching the :class:`Document` schema.
Output is a JSON object matching :class:`RerankResult`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from argus_rerank import DependenceAwareReranker, Document, __version__


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="argus-rerank",
        description="ARGUS-Rerank: dependence-aware reranking for RAG.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ARGUS-Rerank {__version__}",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    rerank = sub.add_parser("rerank", help="Re-rank a candidate document set.")
    rerank.add_argument("--query", required=True, help="The query string.")
    rerank.add_argument(
        "--documents",
        required=True,
        type=Path,
        help="Path to a JSON array of Document objects.",
    )
    rerank.add_argument(
        "--query-class",
        default="default",
        help="Query class label for per-class calibration. Defaults to 'default'.",
    )
    rerank.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output file path. Writes to stdout if omitted.",
    )
    rerank.add_argument(
        "--explain",
        action="store_true",
        help="Print a human-readable explanation instead of JSON.",
    )

    return parser


def _load_documents(path: Path) -> list[Document]:
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    if not isinstance(raw, list):
        raise SystemExit(f"Expected JSON array in {path}; got {type(raw).__name__}")
    return [Document.model_validate(item) for item in raw]


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "rerank":
        return _cmd_rerank(args)

    parser.print_help()
    return 2


def _cmd_rerank(args: argparse.Namespace) -> int:
    documents = _load_documents(args.documents)
    reranker = DependenceAwareReranker()
    result = reranker.rerank(
        query=args.query,
        documents=documents,
        query_class=args.query_class,
    )

    if args.explain:
        text = result.explain()
        if args.output:
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0

    payload = json.dumps(result.model_dump(mode="json"), indent=2, default=str)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        sys.stdout.write(payload + "\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
