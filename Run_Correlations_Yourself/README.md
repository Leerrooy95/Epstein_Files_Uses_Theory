# Run Correlations Yourself

**Purpose:** Independent verification scripts for the reported correlations.

**Last Updated:** February 9, 2026

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Reproduce the three ORIGINAL correlations (pre-2026 datasets)
python run_original_analysis.py
```

---

## Scripts in This Folder

| Script | What It Reproduces | Datasets Used |
|--------|-------------------|---------------|
| `run_original_analysis.py` | Part 1: r = 0.6196 (2-week lag, 30 weeks)<br>Part 2: Mann-Whitney U p = 0.002<br>Part 3: χ² = 330.62 (14-day periodicity) | Original pre-2026 CSVs from `Control_Proof/`, `Project_Trident/`, `09_Silicon_Sovereignty/` |

---

## Reported Correlations

| # | Correlation | Stat | Datasets | Script |
|---|-------------|------|----------|--------|
| 1 | Reflexive Control (2-week lag) | r = 0.6196 | 30-row master CSV | `run_original_analysis.py` Part 1 |
| 2 | Project Trident (ritual vs holiday proximity) | p = 0.002 | 533-row lag CSV | `run_original_analysis.py` Part 2 |
| 3 | Multi-Dataset Cross-Validation (14-day periodicity) | χ² = 330.62 | 4 Silicon Sovereignty CSVs (2,102 records) | `run_original_analysis.py` Part 3 |

---

## Robustness Tests

For the full robustness test suite (permutation, autocorrelation adjustment, Dec 2025 exclusion, rolling-window, event-study, Granger causality), see:

```bash
cd Project_Trident/Copilot_Opus_4.6_Analysis/Statistical_Tests/
python permutation_test.py                   # Shuffle-based significance
python autocorrelation_adjusted_test.py      # Block bootstrap
python normalized_correlation.py             # Per-year normalized correlation
python cross_validation_dec2025.py           # Dec 2025 exclusion test
python rolling_window_correlation.py         # Sliding-window analysis
python event_study_framework.py              # Compliance response analysis
python granger_causality_test.py             # Predictive direction test
```

---

## Wrong_Correlations/ Subfolder

The `Wrong_Correlations/` subfolder contains archived scripts that are preserved for transparency:

- **`reproduce_updated_correlation.py`** — ⚠️ DEPRECATED. Previously produced r = 0.6685 using New_Data_2026 datasets. This correlation was produced in early January 2026 when the user accidentally mixed New_Data_2026 datasets into verification scripts. This was a user dataset-mixing error, not an AI computation error.
- **`reproduce_original_correlation.py`** and **`independent_statistical_verification.py`** — Had hardcoded paths to `/home/user/Epstein_Files_Uses_Theory/New_Data_2026/` instead of using relative paths to the correct original datasets.
- **`run_original_analysis.py`** — Archived copy (the corrected version is in the main folder).
- **`DISCREPANCY_ANALYSIS.md`** — Methodology comparison (still informative for understanding the r = 0.6685 → r = 0.6192 discrepancy).

---

*Last updated: February 9, 2026*
