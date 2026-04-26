"""Tests for the calibration layer."""

from __future__ import annotations

import numpy as np

from argus_rerank.calibration import (
    CalibrationRegistry,
    IsotonicCalibrator,
    PlattCalibrator,
    SupportFeatures,
)


def _features(effective_n: float, n_independent: int = 1) -> SupportFeatures:
    return SupportFeatures(
        effective_n=effective_n,
        naive_count=max(1, int(effective_n)),
        independence_ratio=1.0 if int(effective_n) == 0 else 1.0,
        mean_weight=0.7,
        max_weight=0.9,
        n_independent_documents=n_independent,
    )


class TestSupportFeatures:
    def test_to_array_has_expected_shape(self) -> None:
        f = _features(2.0)
        arr = f.to_array()
        assert arr.shape == (6,)

    def test_from_per_document_weights(self) -> None:
        f = SupportFeatures.from_per_document_weights(
            weights={"a": 1.0, "b": 0.5, "c": 0.2},
            effective_n=1.4,
            n_independent_documents=2,
        )
        assert f.naive_count == 3
        assert f.max_weight == 1.0
        assert f.n_independent_documents == 2


class TestUnfittedRegistry:
    def test_default_predicts_in_range(self) -> None:
        reg = CalibrationRegistry()
        f = _features(1.0)
        p = reg.predict(f)
        assert 0.0 <= p <= 1.0

    def test_more_evidence_higher_default_score(self) -> None:
        reg = CalibrationRegistry()
        low = reg.predict(_features(0.5, n_independent=0))
        high = reg.predict(_features(5.0, n_independent=4))
        assert high > low

    def test_unknown_class_falls_back_to_default(self) -> None:
        reg = CalibrationRegistry()
        f = _features(1.0)
        # Should not raise and should return same as default.
        p1 = reg.predict(f, query_class="unknown_class")
        p2 = reg.predict(f, query_class="default")
        assert p1 == p2


class TestIsotonicCalibrator:
    def test_fit_and_predict(self) -> None:
        rng = np.random.default_rng(42)
        Xrows = []
        ys = []
        for _ in range(60):
            n_eff = rng.uniform(0.0, 5.0)
            true_p = 1.0 / (1.0 + np.exp(-(n_eff - 2.0)))
            label = float(rng.uniform() < true_p)
            Xrows.append(_features(n_eff, n_independent=int(n_eff)).to_array())
            ys.append(label)
        X = np.stack(Xrows)
        y = np.array(ys)

        cal = IsotonicCalibrator()
        cal.fit(X, y)
        assert cal.is_fitted
        preds = cal.predict(X)
        assert preds.shape == (60,)
        assert np.all(preds >= 0.0) and np.all(preds <= 1.0)


class TestPlattCalibrator:
    def test_fit_and_predict(self) -> None:
        rng = np.random.default_rng(7)
        Xrows = []
        ys = []
        for _ in range(40):
            n_eff = rng.uniform(0.0, 5.0)
            label = 1 if n_eff > 2.0 else 0
            Xrows.append(_features(n_eff, n_independent=int(n_eff)).to_array())
            ys.append(label)
        X = np.stack(Xrows)
        y = np.array(ys)

        cal = PlattCalibrator()
        cal.fit(X, y)
        assert cal.is_fitted
        preds = cal.predict(X)
        assert preds.shape == (40,)


class TestCalibrationRegistryPersistence:
    def test_save_and_load_round_trip(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        reg = CalibrationRegistry()

        rng = np.random.default_rng(0)
        feats = []
        labels = []
        for _ in range(40):
            n_eff = rng.uniform(0.0, 5.0)
            feats.append(_features(n_eff, n_independent=int(n_eff)))
            labels.append(1 if n_eff > 2.0 else 0)
        reg.fit("factual", feats, labels)

        path = tmp_path / "calibrators.pkl"
        reg.save(path)

        loaded = CalibrationRegistry.load(path)
        assert loaded.is_fitted("factual")

        f = _features(3.0, n_independent=3)
        # Round-trip predictions should be identical (deterministic).
        assert reg.predict(f, "factual") == loaded.predict(f, "factual")
