"""Tests for copy-language detection."""

from __future__ import annotations

from argus_rerank.copy_detection import (
    CopyDetectionConfig,
    copy_signal_strength,
    longest_common_ngram_run,
    ngram_jaccard,
)


class TestNgramJaccard:
    def test_identical(self) -> None:
        text = "the quick brown fox jumps over the lazy dog very quickly today"
        assert ngram_jaccard(text, text, n=5) == 1.0

    def test_disjoint(self) -> None:
        a = "alpha beta gamma delta epsilon zeta"
        b = "one two three four five six seven"
        assert ngram_jaccard(a, b, n=5) == 0.0

    def test_partial(self) -> None:
        a = "the quick brown fox jumps over the lazy dog one fine morning today"
        b = "the quick brown fox jumps over the lazy dog after the rain stopped"
        score = ngram_jaccard(a, b, n=5)
        assert 0.0 < score < 1.0


class TestLongestCommonRun:
    def test_finds_long_verbatim_span(self) -> None:
        a = (
            "The committee resolved that customer funds were not segregated "
            "from Alameda accounts."
        )
        b = (
            "It is well established that customer funds were not segregated "
            "from Alameda accounts at any time."
        )
        run = longest_common_ngram_run(a, b, min_n=5)
        assert run >= 5

    def test_below_threshold_returns_zero(self) -> None:
        a = "this is a very short sentence"
        b = "completely unrelated text content here goes another sentence too"
        run = longest_common_ngram_run(a, b, min_n=10)
        assert run == 0

    def test_short_input_returns_zero(self) -> None:
        a = "tiny"
        b = "also tiny"
        run = longest_common_ngram_run(a, b, min_n=5)
        assert run == 0


class TestCopySignalStrength:
    def test_full_copy_high_strength(self) -> None:
        text = (
            "The board approved the merger after extensive due diligence "
            "and consultation with outside counsel and financial advisors."
        )
        signal = copy_signal_strength(text, text)
        assert signal.strength >= 0.9
        assert signal.ngram_jaccard >= 0.9

    def test_paraphrase_intermediate_strength(self) -> None:
        a = (
            "The board approved the merger after extensive due diligence "
            "and consultation with outside counsel and financial advisors."
        )
        b = (
            "Following extensive due diligence and consultations with external "
            "counsel and bankers, the board greenlit the merger."
        )
        signal = copy_signal_strength(a, b)
        # Should be detectably more than 0 but less than full mirror.
        assert signal.strength < 0.9

    def test_unrelated_low_strength(self) -> None:
        a = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu"
        b = "one two three four five six seven eight nine ten eleven twelve"
        signal = copy_signal_strength(a, b)
        assert signal.strength < 0.1

    def test_quote_with_attribution_detected_via_run(self) -> None:
        """Even if Jaccard is moderate, a long verbatim span should max out the
        run-based component of the signal."""
        config = CopyDetectionConfig()
        a = (
            "FTX customer funds were not segregated from Alameda Research's trading "
            "accounts; investigators found commingled balances."
        )
        b = (
            "Per a recent report, FTX customer funds were not segregated from Alameda "
            "Research's trading accounts; analysts continue to investigate."
        )
        signal = copy_signal_strength(a, b, config)
        assert signal.longest_common_run >= 8
        assert signal.strength > 0.2
