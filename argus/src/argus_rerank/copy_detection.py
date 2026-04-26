"""Copy-language detection via overlapping n-gram signatures.

Complements MinHash with a more sensitive signal: contiguous n-gram overlap.
A document that quotes or paraphrases a long verbatim span will share many
contiguous high-order n-grams even when the surrounding language differs. This
is a useful signal for ``QUOTE_OF`` and ``DERIVED_FROM`` edges that pure
Jaccard might miss.

Statement-class tags
--------------------
- :func:`ngram_jaccard` — Definition: classical Jaccard similarity over
  contiguous n-gram sets.
- :func:`longest_common_ngram_run` — Engineering rule. The "long contiguous
  span" heuristic for paraphrase detection is widely used (Brin/Davis/Garcia-Molina
  1995; SCAM) but the specific cutoffs in :class:`CopyDetectionConfig` are
  empirical defaults, not theorems.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)


def _tokens(text: str) -> list[str]:
    return _TOKEN_PATTERN.findall(text.lower())


def _ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    if len(tokens) < n:
        return []
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def ngram_jaccard(text_a: str, text_b: str, n: int = 5) -> float:
    """Jaccard similarity of n-gram sets. Returns 0.0 if either is empty."""
    a = set(_ngrams(_tokens(text_a), n))
    b = set(_ngrams(_tokens(text_b), n))
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def longest_common_ngram_run(text_a: str, text_b: str, min_n: int = 5) -> int:
    """Length, in tokens, of the longest contiguous span shared by both texts.

    Returns 0 if no span of at least ``min_n`` consecutive tokens is shared.

    This catches verbatim copy-paste even when surrounding sentences are heavily
    rewritten — a typical citation-laundering pattern.
    """
    tokens_a = _tokens(text_a)
    tokens_b = _tokens(text_b)
    if len(tokens_a) < min_n or len(tokens_b) < min_n:
        return 0

    # Standard dynamic-programming longest common substring on token arrays,
    # but space-efficient (O(min(|a|, |b|)) with a rolling buffer).
    if len(tokens_a) > len(tokens_b):
        tokens_a, tokens_b = tokens_b, tokens_a  # ensure a is shorter

    prev = [0] * (len(tokens_a) + 1)
    curr = [0] * (len(tokens_a) + 1)
    best = 0
    for j in range(1, len(tokens_b) + 1):
        for i in range(1, len(tokens_a) + 1):
            if tokens_a[i - 1] == tokens_b[j - 1]:
                curr[i] = prev[i - 1] + 1
                best = max(best, curr[i])
            else:
                curr[i] = 0
        prev, curr = curr, prev
        for k in range(len(curr)):
            curr[k] = 0

    return best if best >= min_n else 0


@dataclass(frozen=True)
class CopyDetectionConfig:
    """Thresholds for copy-language inference."""

    ngram_size: int = 5
    """Order of n-grams used for the Jaccard score."""

    jaccard_quote_threshold: float = 0.18
    """Jaccard >= this threshold contributes a QUOTE_OF signal."""

    jaccard_mirror_threshold: float = 0.55
    """Jaccard >= this threshold contributes a MIRRORS signal (very high overlap)."""

    min_span_for_quote: int = 8
    """A contiguous shared span >= this many tokens contributes a QUOTE_OF signal
    even when overall Jaccard is low (citation-laundering case)."""


@dataclass(frozen=True)
class CopySignal:
    """Output of :func:`copy_signal_strength`. Strength is in [0, 1]."""

    ngram_jaccard: float
    longest_common_run: int
    strength: float
    """Aggregate copy-detection score in [0, 1] used to weight dependence edges."""


def copy_signal_strength(
    text_a: str,
    text_b: str,
    config: CopyDetectionConfig | None = None,
) -> CopySignal:
    """Compute a copy-detection signal strength for two texts.

    The aggregate ``strength`` is the maximum of:
      - n-gram Jaccard, scaled by the mirror threshold (so ``mirror_threshold``
        Jaccard maps to 1.0 strength)
      - the longest common token run divided by 32 (so a 32-token verbatim
        copy alone is enough to max out the signal)

    All scores are clipped to [0, 1].
    """
    cfg = config or CopyDetectionConfig()
    j = ngram_jaccard(text_a, text_b, n=cfg.ngram_size)
    run = longest_common_ngram_run(text_a, text_b, min_n=cfg.min_span_for_quote)

    jaccard_component = min(1.0, j / cfg.jaccard_mirror_threshold) if cfg.jaccard_mirror_threshold > 0 else 0.0
    run_component = min(1.0, run / 32.0)
    strength = max(jaccard_component, run_component)

    return CopySignal(
        ngram_jaccard=j,
        longest_common_run=run,
        strength=strength,
    )
