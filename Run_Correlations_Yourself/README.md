# Run Correlations Yourself

**Purpose:** Independent verification scripts for all reported correlations.

**Last Updated:** February 9, 2026

---

## ⚠️ Important: Dataset Correction (February 2026)

The original scripts in this folder had been using the **wrong datasets** for some correlations. Specifically, the January 2026 verification scripts (`reproduce_original_correlation.py` and `independent_statistical_verification.py`) used the `New_Data_2026/` files instead of the original pre-2026 datasets.

The incorrect scripts have been moved to `Wrong_Correlations/` for transparency. The corrected scripts are here in the main folder.

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Reproduce the three ORIGINAL correlations (pre-2026 datasets)
python run_original_analysis.py

# Reproduce the UPDATED correlations (New_Data_2026 datasets)
python reproduce_updated_correlation.py
```

---

## Scripts in This Folder

| Script | What It Reproduces | Datasets Used |
|--------|-------------------|---------------|
| `run_original_analysis.py` | Part 1: r = 0.6196 (2-week lag, 30 weeks)<br>Part 2: Mann-Whitney U p = 0.002<br>Part 3: χ² = 330.62 (14-day periodicity) | Original pre-2026 CSVs from `Control_Proof/`, `Project_Trident/`, `09_Silicon_Sovereignty/` |
| `reproduce_updated_correlation.py` | Core scope: r ≈ 0.6192 (target 0.6685)<br>Full scope: r ≈ 0.5268 | `New_Data_2026/` CSVs (uploaded January 4, 2026) |

---

## All Five Reported Correlations

| # | Correlation | Stat | Datasets | Script |
|---|-------------|------|----------|--------|
| 1 | Reflexive Control (2-week lag) | r = 0.6196 | 30-row master CSV | `run_original_analysis.py` Part 1 |
| 2 | Project Trident (ritual vs holiday proximity) | p = 0.002 | 533-row lag CSV | `run_original_analysis.py` Part 2 |
| 3 | Multi-Dataset Cross-Validation (14-day periodicity) | χ² = 330.62 | 4 Silicon Sovereignty CSVs (2,105 records) | `run_original_analysis.py` Part 3 |
| 4 | Updated event-count (core scope, 0-lag) | r = 0.6685 | 5 New_Data_2026 CSVs (~1,010 events) | `reproduce_updated_correlation.py` |
| 5 | Updated event-count (full scope, 0-lag) | r = 0.5268 | 6 New_Data_2026 CSVs (~2,069 events) | `reproduce_updated_correlation.py` |

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

The `Wrong_Correlations/` subfolder contains the **original scripts** that were in this folder before the dataset correction. They are preserved for transparency. See `Wrong_Correlations/README.md` for details on what went wrong.

**Key issue:** `reproduce_original_correlation.py` and `independent_statistical_verification.py` had hardcoded paths to `/home/user/Epstein_Files_Uses_Theory/New_Data_2026/` instead of using relative paths to the correct original datasets.

---

*Last updated: February 9, 2026*
