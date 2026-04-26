"""Near-duplicate detection using SimHash and MinHash.

Two complementary techniques. SimHash gives fast Hamming-distance comparison
suited to short documents and high-precision exact-paraphrase detection. MinHash
+ LSH (via :mod:`datasketch`) handles longer documents and detects substantial
shared content even when surface order differs.

Statement-class tags
--------------------
- :class:`SimHasher` — Engineering rule. SimHash thresholds are heuristic and
  configurable; they are not theorems.
- :func:`minhash_jaccard` — Empirical estimator for Jaccard similarity of
  shingled token sets. Theoretical accuracy bounds are known (Broder 1997)
  but we expose them as engineering constants, not as proven properties of
  this implementation.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable
from dataclasses import dataclass

from datasketch import MinHash, MinHashLSH

_TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    """Lowercase word-token split. Adequate for English news/legal/technical text."""
    return _TOKEN_PATTERN.findall(text.lower())


def _shingle(tokens: list[str], n: int) -> set[str]:
    """Generate n-gram shingles from tokens. Empty token list yields empty set."""
    if len(tokens) < n:
        # Treat short docs as a single shingle so they still hash to something.
        return {" ".join(tokens)} if tokens else set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


# --- SimHash ----------------------------------------------------------------


def _hash_to_bits(token: str, num_bits: int) -> list[int]:
    """Hash a token to a fixed-width bit vector. Uses BLAKE2b for speed/stability."""
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=(num_bits + 7) // 8).digest()
    bits: list[int] = []
    for byte in digest:
        for i in range(8):
            if len(bits) >= num_bits:
                return bits
            bits.append((byte >> i) & 1)
    return bits


@dataclass(frozen=True)
class SimHashConfig:
    """Configuration for SimHash near-duplicate detection."""

    num_bits: int = 64
    """Width of the SimHash signature in bits. 64 is the canonical default."""

    shingle_size: int = 3
    """Token n-gram width. 3 is a robust default for English prose."""

    hamming_threshold: int = 6
    """Documents within this Hamming distance are considered near-duplicates.
    Charikar 2002 / Manku 2007 use 3 for web-scale dedup; we default higher
    because RAG retrieval surfaces are smaller and we prefer recall here."""


class SimHasher:
    """Compute and compare 64-bit SimHash signatures."""

    def __init__(self, config: SimHashConfig | None = None) -> None:
        self.config = config or SimHashConfig()

    def fingerprint(self, text: str) -> int:
        """Return the SimHash fingerprint of ``text`` as an integer."""
        tokens = _tokenize(text)
        shingles = _shingle(tokens, self.config.shingle_size)
        if not shingles:
            return 0

        v = [0] * self.config.num_bits
        for shingle in shingles:
            bits = _hash_to_bits(shingle, self.config.num_bits)
            for i, bit in enumerate(bits):
                v[i] += 1 if bit == 1 else -1

        fingerprint = 0
        for i, accum in enumerate(v):
            if accum > 0:
                fingerprint |= 1 << i
        return fingerprint

    @staticmethod
    def hamming_distance(a: int, b: int) -> int:
        """Number of differing bits between two SimHash fingerprints."""
        return (a ^ b).bit_count()

    def is_near_duplicate(self, text_a: str, text_b: str) -> bool:
        """True iff Hamming distance between fingerprints is within threshold."""
        a = self.fingerprint(text_a)
        b = self.fingerprint(text_b)
        return self.hamming_distance(a, b) <= self.config.hamming_threshold

    def similarity(self, text_a: str, text_b: str) -> float:
        """Return a similarity score in [0, 1] derived from Hamming distance.

        We use ``1 - hamming / num_bits``. This is monotonic in Hamming distance
        and bounded; the absolute scale is not directly comparable to Jaccard.
        """
        a = self.fingerprint(text_a)
        b = self.fingerprint(text_b)
        h = self.hamming_distance(a, b)
        return max(0.0, 1.0 - h / self.config.num_bits)


# --- MinHash + LSH ----------------------------------------------------------


@dataclass(frozen=True)
class MinHashConfig:
    """Configuration for MinHash + LSH near-duplicate detection."""

    num_perm: int = 128
    """Number of permutations. 128 gives ~0.04 RMSE on Jaccard estimation."""

    shingle_size: int = 3
    """Token n-gram width."""

    jaccard_threshold: float = 0.5
    """LSH bucketing threshold. Pairs with estimated Jaccard at or above this
    are surfaced as candidates."""


def _build_minhash(text: str, num_perm: int, shingle_size: int) -> MinHash:
    mh = MinHash(num_perm=num_perm)
    tokens = _tokenize(text)
    shingles = _shingle(tokens, shingle_size)
    for s in shingles:
        mh.update(s.encode("utf-8"))
    return mh


def minhash_jaccard(text_a: str, text_b: str, config: MinHashConfig | None = None) -> float:
    """Estimated Jaccard similarity between two texts via MinHash."""
    cfg = config or MinHashConfig()
    a = _build_minhash(text_a, cfg.num_perm, cfg.shingle_size)
    b = _build_minhash(text_b, cfg.num_perm, cfg.shingle_size)
    return float(a.jaccard(b))


class MinHashLSHIndex:
    """Wrapper over :class:`datasketch.MinHashLSH` for batch near-duplicate detection."""

    def __init__(self, config: MinHashConfig | None = None) -> None:
        self.config = config or MinHashConfig()
        self._lsh = MinHashLSH(
            threshold=self.config.jaccard_threshold,
            num_perm=self.config.num_perm,
        )
        self._signatures: dict[str, MinHash] = {}

    def insert(self, doc_id: str, text: str) -> None:
        mh = _build_minhash(text, self.config.num_perm, self.config.shingle_size)
        self._signatures[doc_id] = mh
        if doc_id in self._lsh:  # pragma: no cover — defensive idempotency.
            self._lsh.remove(doc_id)
        self._lsh.insert(doc_id, mh)

    def candidates_for(self, doc_id: str) -> list[str]:
        """Return ids of indexed documents likely to share Jaccard >= threshold."""
        mh = self._signatures.get(doc_id)
        if mh is None:
            return []
        return [c for c in self._lsh.query(mh) if c != doc_id]

    def all_candidate_pairs(self) -> Iterable[tuple[str, str, float]]:
        """Yield ``(id_a, id_b, jaccard)`` for each candidate near-duplicate pair.

        Each unordered pair is yielded once, with ``id_a < id_b`` lexicographically.
        """
        seen: set[tuple[str, str]] = set()
        for doc_id in self._signatures:
            for cand in self.candidates_for(doc_id):
                pair = (doc_id, cand) if doc_id < cand else (cand, doc_id)
                if pair in seen:
                    continue
                seen.add(pair)
                jaccard = float(self._signatures[pair[0]].jaccard(self._signatures[pair[1]]))
                yield pair[0], pair[1], jaccard
