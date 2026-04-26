
### 8.3 Wedge 3 — Calibration layer for forensic claims

**Status:** TERTIARY WEDGE. Ship at month 12+ as part of full ARGUS reference architecture release, not as a standalone first.

**Why not first:** Calibration requires labeled validation data, which requires the rest of the system to be running and a real query workload to score. As Lane 3 noted, this is NEEDS_PROTOTYPE_FIRST.

**One-line definition:** A calibrator that maps support + grounding + dependence + uncertainty features into calibrated decision probabilities for forensic claims, with per-query-class evaluation via Brier / ECE / reliability diagrams / selective risk.

**Closest published cousin:** Mohri & Hashimoto 2024 (Conformal LM Factuality Guarantees). Differentiate by: (a) per-query-class calibration, (b) integration with dependence-aware corroboration features, (c) selective-prediction interface.

**Defer until V13 ships and the wedge ecosystem is in place.**

