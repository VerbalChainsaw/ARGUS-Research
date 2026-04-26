"""Calibration layer: support → calibrated claim confidence.

Maps a feature vector derived from C_eff and dependence statistics into a
calibrated probability in [0, 1] using isotonic regression (default) or
Platt scaling. Per ARGUS Codex §3.9, calibration must be evaluated per
query class; this module exposes a per-class registry so callers can fit
separate calibrators per ``query_class`` label.

Statement-class
---------------
- :func:`UncalibratedSupport` -> :func:`CalibratedConfidence` is an
  Empirical hypothesis: that a low-dimensional summary of C_eff plus
  dependence statistics is sufficient to produce a usefully calibrated
  scalar confidence. The hypothesis is falsifiable via reliability
  diagrams and ECE on held-out data per ARGUS Codex W-3.
- The default unfitted "logistic-saturation" mapping is an Engineering
  rule, not a theorem. It exists so the library produces sensible values
  before any calibrator has been fit.
"""

from __future__ import annotations

import math
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression


@dataclass(frozen=True)
class SupportFeatures:
    """Compact feature vector summarizing a reranking call's support evidence.

    All features are dimensionless and live in [0, ∞) or [0, 1] as documented.
    """

    effective_n: float
    """C_eff: effective independent-source count."""

    naive_count: int
    """Number of input documents."""

    independence_ratio: float
    """``effective_n / max(1, naive_count)`` — fraction of evidence that is
    actually independent. Lives in [0, 1]."""

    mean_weight: float
    """Mean per-document weight after dependence discounting. Lives in [0, 1]."""

    max_weight: float
    """Best per-document weight. Lives in [0, 1]."""

    n_independent_documents: int
    """Number of documents whose incoming-edge max-weight is below 0.25."""

    @classmethod
    def from_per_document_weights(
        cls,
        weights: dict[str, float],
        effective_n: float,
        n_independent_documents: int,
    ) -> SupportFeatures:
        n = max(1, len(weights))
        mean_w = sum(weights.values()) / n if weights else 0.0
        max_w = max(weights.values()) if weights else 0.0
        return cls(
            effective_n=float(effective_n),
            naive_count=n,
            independence_ratio=float(effective_n) / float(n),
            mean_weight=float(mean_w),
            max_weight=float(max_w),
            n_independent_documents=int(n_independent_documents),
        )

    def to_array(self) -> np.ndarray:
        """Return the feature vector as a numpy array."""
        return np.array(
            [
                self.effective_n,
                float(self.naive_count),
                self.independence_ratio,
                self.mean_weight,
                self.max_weight,
                float(self.n_independent_documents),
            ],
            dtype=float,
        )


def _logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _default_score(features: SupportFeatures) -> float:
    """Reasonable default score before any calibrator has been fit.

    The mapping is a logistic over a hand-crafted linear combination of the
    most informative features. It exists so that out-of-the-box use produces
    plausible numbers; production deployments are expected to fit a calibrator
    on labeled data and supersede this.
    """
    z = (
        -2.0
        + 1.4 * math.log1p(features.effective_n)
        + 1.5 * features.independence_ratio
        + 0.6 * features.max_weight
        + 0.25 * math.log1p(features.n_independent_documents)
    )
    return _logistic(z)


# --- Calibrators ------------------------------------------------------------


class _BaseCalibrator:
    """Abstract base for fittable calibrators."""

    is_fitted: bool

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class IsotonicCalibrator(_BaseCalibrator):
    """One-dimensional isotonic regression on a scalar uncalibrated score.

    Fits ``y_true ~ Isotonic(score(X))``, where ``score`` is the default
    logistic feature combiner above. Robust to non-linearity in the
    underlying feature -> probability relationship.
    """

    def __init__(self) -> None:
        self.is_fitted = False
        self._iso: IsotonicRegression | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        if X.ndim != 2 or X.shape[1] != 6:
            raise ValueError(f"Expected X.shape[1]==6, got {X.shape}")
        if y.ndim != 1 or y.shape[0] != X.shape[0]:
            raise ValueError("y must be 1-D with the same length as X")
        scores = np.array([_default_score(_features_from_array(row)) for row in X])
        self._iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
        self._iso.fit(scores, y.astype(float))
        self.is_fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted or self._iso is None:
            return np.array([_default_score(_features_from_array(row)) for row in X])
        scores = np.array([_default_score(_features_from_array(row)) for row in X])
        out: np.ndarray = self._iso.predict(scores)
        clipped: np.ndarray = np.clip(out, 0.0, 1.0)
        return clipped


class PlattCalibrator(_BaseCalibrator):
    """Logistic-regression calibrator fit on the full feature vector."""

    def __init__(self, C: float = 1.0) -> None:
        self.is_fitted = False
        self._lr: LogisticRegression | None = None
        self._C = C

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        if X.ndim != 2 or X.shape[1] != 6:
            raise ValueError(f"Expected X.shape[1]==6, got {X.shape}")
        unique = np.unique(y)
        if unique.size < 2:
            raise ValueError(
                "PlattCalibrator requires y to contain at least two classes."
            )
        self._lr = LogisticRegression(C=self._C, max_iter=1000)
        self._lr.fit(X, y.astype(int))
        self.is_fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted or self._lr is None:
            return np.array([_default_score(_features_from_array(row)) for row in X])
        proba: np.ndarray = self._lr.predict_proba(X)[:, 1]
        clipped: np.ndarray = np.clip(proba, 0.0, 1.0)
        return clipped


def _features_from_array(arr: np.ndarray) -> SupportFeatures:
    return SupportFeatures(
        effective_n=float(arr[0]),
        naive_count=int(arr[1]),
        independence_ratio=float(arr[2]),
        mean_weight=float(arr[3]),
        max_weight=float(arr[4]),
        n_independent_documents=int(arr[5]),
    )


# --- Registry --------------------------------------------------------------


CalibratorKind = Literal["isotonic", "platt"]


def _new_calibrator(kind: CalibratorKind) -> _BaseCalibrator:
    if kind == "isotonic":
        return IsotonicCalibrator()
    if kind == "platt":
        return PlattCalibrator()
    raise ValueError(f"Unknown calibrator kind: {kind!r}")


class CalibrationRegistry:
    """Per-query-class registry of calibrators.

    Per ARGUS Codex §3.9, calibration must be evaluated and fit per query
    class. The registry stores calibrators keyed by an arbitrary string label
    (e.g., ``"factual"``, ``"interpretive"``, ``"forensic-employment"``) and
    falls back to the ``"default"`` calibrator when the class is unknown.
    """

    def __init__(self, default_kind: CalibratorKind = "isotonic") -> None:
        self._default_kind: CalibratorKind = default_kind
        self._calibrators: dict[str, _BaseCalibrator] = {
            "default": _new_calibrator(default_kind)
        }

    def fit(
        self,
        query_class: str,
        features: list[SupportFeatures],
        labels: list[float] | list[int] | np.ndarray,
        kind: CalibratorKind | None = None,
    ) -> None:
        """Fit a calibrator for ``query_class`` on (features, labels) pairs."""
        if not features:
            raise ValueError("features must be non-empty")
        cal = _new_calibrator(kind or self._default_kind)
        X = np.stack([f.to_array() for f in features])
        y = np.asarray(labels, dtype=float)
        cal.fit(X, y)
        self._calibrators[query_class] = cal

    def predict(
        self,
        features: SupportFeatures,
        query_class: str = "default",
    ) -> float:
        cal = self._calibrators.get(query_class, self._calibrators["default"])
        out = cal.predict(features.to_array().reshape(1, -1))
        return float(out[0])

    def is_fitted(self, query_class: str = "default") -> bool:
        cal = self._calibrators.get(query_class, self._calibrators["default"])
        return cal.is_fitted

    def save(self, path: str | Path) -> None:
        """Persist the registry to disk via pickle."""
        with open(path, "wb") as fh:
            pickle.dump(
                {
                    "default_kind": self._default_kind,
                    "calibrators": self._calibrators,
                },
                fh,
            )

    @classmethod
    def load(cls, path: str | Path) -> CalibrationRegistry:
        """Restore a registry previously saved with :meth:`save`."""
        with open(path, "rb") as fh:
            blob: dict[str, Any] = pickle.load(fh)
        registry = cls(default_kind=blob["default_kind"])
        registry._calibrators = blob["calibrators"]
        return registry
