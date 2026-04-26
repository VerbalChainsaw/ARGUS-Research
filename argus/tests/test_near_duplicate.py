"""Tests for near-duplicate detection."""

from __future__ import annotations

import pytest

from argus_rerank.near_duplicate import (
    MinHashConfig,
    MinHashLSHIndex,
    SimHashConfig,
    SimHasher,
    minhash_jaccard,
)


class TestSimHasher:
    def test_identical_text_zero_distance(self) -> None:
        hasher = SimHasher()
        text = "The quick brown fox jumps over the lazy dog."
        a = hasher.fingerprint(text)
        b = hasher.fingerprint(text)
        assert hasher.hamming_distance(a, b) == 0
        assert hasher.similarity(text, text) == 1.0

    def test_unrelated_text_high_distance(self) -> None:
        hasher = SimHasher()
        a = "The quick brown fox jumps over the lazy dog."
        b = "Quantum chromodynamics describes strong nuclear force interactions."
        assert hasher.similarity(a, b) < 0.85

    def test_paraphrase_lower_distance_than_unrelated(self) -> None:
        hasher = SimHasher()
        original = "The quick brown fox jumps over the lazy dog one sunny morning."
        paraphrase = "A quick brown fox leapt over a lazy dog one sunny morning."
        unrelated = "Quantum chromodynamics describes nuclear interactions."

        assert hasher.similarity(original, paraphrase) > hasher.similarity(
            original, unrelated
        )

    def test_near_duplicate_threshold(self) -> None:
        """Near-duplicates should be detected within the default threshold."""
        hasher = SimHasher(SimHashConfig(hamming_threshold=10))
        a = "The fox jumped over the lazy dog at noon on Tuesday."
        b = "The fox jumped over the lazy dog at noon on Tuesday."
        assert hasher.is_near_duplicate(a, b)

    def test_empty_text_returns_zero_fingerprint(self) -> None:
        hasher = SimHasher()
        assert hasher.fingerprint("") == 0


class TestMinHashJaccard:
    def test_identical_high_jaccard(self) -> None:
        text = "this is some text about a test that we are running"
        j = minhash_jaccard(text, text)
        assert j > 0.9

    def test_disjoint_low_jaccard(self) -> None:
        a = "alpha beta gamma delta epsilon zeta eta theta"
        b = "one two three four five six seven eight nine ten"
        j = minhash_jaccard(a, b)
        assert j < 0.1

    def test_partial_overlap_intermediate(self) -> None:
        a = "this is the first half and this is the common shared phrase"
        b = "this is the common shared phrase and this is the second half"
        j = minhash_jaccard(a, b)
        assert 0.05 < j < 0.95


class TestMinHashLSHIndex:
    def test_finds_near_duplicate_pairs(self) -> None:
        idx = MinHashLSHIndex(MinHashConfig(jaccard_threshold=0.3))
        idx.insert("a", "the fox jumped over the lazy dog at noon on tuesday")
        idx.insert("b", "the fox jumped over the lazy dog at noon on tuesday")
        idx.insert(
            "c",
            "quantum chromodynamics describes the strong nuclear force interactions",
        )

        candidates_for_a = idx.candidates_for("a")
        assert "b" in candidates_for_a
        assert "c" not in candidates_for_a

    def test_all_candidate_pairs_yields_each_once(self) -> None:
        idx = MinHashLSHIndex(MinHashConfig(jaccard_threshold=0.3))
        text = "shared content shared content shared content"
        idx.insert("a", text)
        idx.insert("b", text)
        idx.insert("c", text)

        pairs = list(idx.all_candidate_pairs())
        # 3 documents -> 3 pairs (a,b) (a,c) (b,c)
        unordered = {tuple(sorted([x, y])) for x, y, _ in pairs}
        assert unordered == {("a", "b"), ("a", "c"), ("b", "c")}


@pytest.mark.parametrize("text", ["", "   ", "\t\n"])
def test_simhash_robust_to_blank_input(text: str) -> None:
    hasher = SimHasher()
    fp = hasher.fingerprint(text)
    assert isinstance(fp, int)
