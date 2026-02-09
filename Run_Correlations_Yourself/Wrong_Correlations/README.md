# ⚠️ Wrong Correlations — Archived for Transparency

**These scripts used the wrong datasets and are preserved here for transparency.**

These files were the original contents of the `Run_Correlations_Yourself/` folder. They were moved here in February 2026 when it was discovered that `reproduce_original_correlation.py` and `independent_statistical_verification.py` used the **New_Data_2026/** datasets (uploaded January 4, 2026) instead of the **original pre-2026 datasets** (uploaded December 22–25, 2025).

---

## What Went Wrong

The original correlations (r = 0.6196 at 2-week lag, Project Trident p = 0.002, χ² = 330.62) were computed in December 2025 using datasets from `Control_Proof/`, `Project_Trident/`, and `09_Silicon_Sovereignty/`.

When the 2026 verification scripts were written in January 2026, they accidentally loaded data from `New_Data_2026/` (BlackRock, Biopharma, Infrastructure, etc.) — files that did not exist when the original correlations were calculated. This led to:

| Script | What It Claims | Actual Dataset Used | Problem |
|--------|---------------|--------------------| --------|
| `reproduce_original_correlation.py` | Reproduces r = 0.6685 | New_Data_2026 CSVs | Used wrong datasets; hardcoded paths to `/home/user/Epstein_Files_Uses_Theory/` |
| `independent_statistical_verification.py` | Full independent verification | New_Data_2026 CSVs | Same wrong paths; includes High_Growth_Companies which inflates event count |
| `original_correlation_test.py` | Reproduces r = 0.6196 | Relative path (works) | ✅ This script was correct, but requires being run from `Control_Proof/` directory |
| `run_original_analysis.py` | Reproduces original analysis | Pre-2026 CSVs (correct) | ✅ This script was correct — uses proper relative paths |
| `DISCREPANCY_ANALYSIS.md` | Explains r = 0.6685 vs r = 0.5268 | N/A | ✅ Analysis is correct — the discrepancy is real and well-explained |

**Note:** `run_original_analysis.py` and `DISCREPANCY_ANALYSIS.md` were actually correct. They were moved here alongside the wrong scripts to keep the folder as a complete historical archive. The corrected versions in the parent folder supersede them.

---

## The Corrected Scripts

The correct correlation scripts are now in the parent folder (`Run_Correlations_Yourself/`). They use:

1. **Original pre-2026 datasets** from `Control_Proof/`, `Project_Trident/`, and `09_Silicon_Sovereignty/`
2. **Relative paths** so they work from any checkout of the repository
3. **The same methodology** documented in `Project_Trident/Copilot_Opus_4.6_Analysis/`

For the full robustness test suite (permutation, autocorrelation adjustment, Dec 2025 exclusion, event-study, Granger causality), see:
```
Project_Trident/Copilot_Opus_4.6_Analysis/Statistical_Tests/
```

---

*Archived February 9, 2026*
