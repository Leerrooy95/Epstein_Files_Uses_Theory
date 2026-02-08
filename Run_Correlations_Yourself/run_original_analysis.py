#!/usr/bin/env python3
"""
Run Original Analysis — Uses ONLY the original datasets from Control_Proof/,
Project_Trident/, and 09_Silicon_Sovereignty/.

The New_Data_2026/ folder was NOT part of the original correlations and should
not be used here. This script reproduces the three core statistical findings
using only the datasets that were documented in the release notes (v3.1–v5.5).

Original Datasets Used:
  1. Control_Proof/master_reflexive_correlation_data.csv        (30 weeks)
  2. Control_Proof/reflexive_control_scraped_data.csv           (OSINT triggers)
  3. Project_Trident/Best_Data_For_Project_Trident/
       Lag_Correlation_Analysis_Verified_Holidays.csv           (533 records)
  4. 09_Silicon_Sovereignty/Coalition_Narrative_Map_2015-2025.csv   (456 records)
  5. 09_Silicon_Sovereignty/VOCA_funding_timeline_clean.csv         (667 records)
  6. 09_Silicon_Sovereignty/Regulatory_Map_Data_CLEANED.csv         (76 records)
  7. 09_Silicon_Sovereignty/REFINED_supercomputer_geopolitics (1).csv (906 records)
"""

import os
import sys
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, chi2_contingency

# ---------------------------------------------------------------------------
# Resolve paths relative to the repository root
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

CONTROL_PROOF = os.path.join(REPO_ROOT, "Control_Proof")
PROJECT_TRIDENT = os.path.join(REPO_ROOT, "Project_Trident")
SILICON_SOV = os.path.join(REPO_ROOT, "09_Silicon_Sovereignty")

# ============================================================================
# PART 1 — Reflexive Control Correlation (r = 0.6196 at 2-week lag)
# Source: v3.1 release (December 22, 2025)
# Dataset: Control_Proof/master_reflexive_correlation_data.csv
# ============================================================================

def part1_reflexive_control():
    print("=" * 80)
    print("PART 1: ORIGINAL REFLEXIVE CONTROL CORRELATION (v3.1)")
    print("=" * 80)

    master_path = os.path.join(CONTROL_PROOF, "master_reflexive_correlation_data.csv")
    scraped_path = os.path.join(CONTROL_PROOF, "reflexive_control_scraped_data.csv")

    if not os.path.exists(master_path):
        print(f"ERROR: {master_path} not found")
        return

    master_df = pd.read_csv(master_path)
    print(f"Loaded master dataset: {len(master_df)} weeks of data")
    print(f"Columns: {list(master_df.columns)}")

    if os.path.exists(scraped_path):
        scraped_df = pd.read_csv(scraped_path)
        print(f"Loaded OSINT scrape: {len(scraped_df)} triggers")
    else:
        print("OSINT scrape file not present — proceeding with master data only.")

    friction = master_df["Epstein_Friction_Index"]
    compliance = master_df["Institutional_Compliance_Index"]

    # Direct (0-lag) correlation
    r_direct, p_direct = pearsonr(friction, compliance)
    print(f"\n0-lag (simultaneous):  r = {r_direct:.4f}, p = {p_direct:.4f}")

    # 2-week lagged correlation (the original finding)
    friction_lagged = friction.shift(2)
    valid = ~friction_lagged.isna()
    r_lagged, p_lagged = pearsonr(friction_lagged[valid], compliance[valid])
    print(f"2-week lag (Friction leads): r = {r_lagged:.4f}, p = {p_lagged:.4f}")

    match = abs(r_lagged - 0.6196) < 0.01
    tag = "VERIFIED" if match else "DISCREPANCY"
    print(f"\n{tag}: Original claim r = 0.6196  |  Reproduced r = {r_lagged:.4f}")

# ============================================================================
# PART 2 — Project Trident Mann-Whitney U (p = 0.002)
# Source: v4.5 release (December 24, 2025)
# Dataset: Project_Trident/Best_Data_For_Project_Trident/
#          Lag_Correlation_Analysis_Verified_Holidays.csv
# ============================================================================

def part2_project_trident():
    print("\n" + "=" * 80)
    print("PART 2: PROJECT TRIDENT — MANN-WHITNEY U TEST (v4.5)")
    print("=" * 80)

    lag_path = os.path.join(
        PROJECT_TRIDENT,
        "Best_Data_For_Project_Trident",
        "Lag_Correlation_Analysis_Verified_Holidays.csv",
    )

    if not os.path.exists(lag_path):
        print(f"ERROR: {lag_path} not found")
        return

    df = pd.read_csv(lag_path)
    print(f"Loaded Project Trident lag data: {len(df)} policy-action events")
    print(f"Columns: {list(df.columns)}")

    if "Ritual_Lag" not in df.columns or "Holiday_Lag" not in df.columns:
        print("ERROR: Expected Ritual_Lag and Holiday_Lag columns")
        return

    ritual_lags = df["Ritual_Lag"].abs()
    holiday_lags = df["Holiday_Lag"].abs()

    print(f"\nRitual lags  — mean: {ritual_lags.mean():.2f}, median: {ritual_lags.median():.2f}")
    print(f"Holiday lags — mean: {holiday_lags.mean():.2f}, median: {holiday_lags.median():.2f}")

    u_stat, p_value = stats.mannwhitneyu(ritual_lags, holiday_lags, alternative="less")
    print(f"\nMann-Whitney U statistic: {u_stat:.2f}")
    print(f"p-value: {p_value:.6f}")

    match = abs(p_value - 0.002) < 0.005
    tag = "VERIFIED" if match else "DISCREPANCY"
    print(f"\n{tag}: Original claim p = 0.002  |  Reproduced p = {p_value:.6f}")

    # Proximity analysis
    for window in [7, 14, 21, 30]:
        r_in = (ritual_lags <= window).mean() * 100
        h_in = (holiday_lags <= window).mean() * 100
        ratio = r_in / h_in if h_in > 0 else float("inf")
        print(f"  Within ±{window}d:  Ritual {r_in:.1f}%  |  Holiday {h_in:.1f}%  |  Ratio {ratio:.1f}x")

# ============================================================================
# PART 3 — Multi-Dataset Cross-Validation (χ² = 330.62)
# Source: v5.5 release (December 25, 2025)
# Datasets (2,105 records total from 09_Silicon_Sovereignty/):
#   Coalition_Narrative_Map       — 456 records
#   VOCA_funding_timeline_clean   — 667 records
#   Regulatory_Map_Data_CLEANED   —  76 records
#   REFINED_supercomputer_geopolitics — 906 records
# ============================================================================

def part3_cross_validation():
    print("\n" + "=" * 80)
    print("PART 3: MULTI-DATASET CROSS-VALIDATION (v5.5)")
    print("=" * 80)

    files = {
        "Coalition_Narrative_Map": os.path.join(SILICON_SOV, "Coalition_Narrative_Map_2015-2025.csv"),
        "VOCA_Funding": os.path.join(SILICON_SOV, "VOCA_funding_timeline_clean.csv"),
        "Regulatory_Map": os.path.join(SILICON_SOV, "Regulatory_Map_Data_CLEANED.csv"),
        "Supercomputer_Geopolitics": os.path.join(SILICON_SOV, "REFINED_supercomputer_geopolitics (1).csv"),
    }

    all_dates = []

    for name, path in files.items():
        if not os.path.exists(path):
            print(f"WARNING: {path} not found — skipping {name}")
            continue

        df = pd.read_csv(path)
        print(f"Loaded {name}: {len(df)} records")

        # Find the date column
        date_col = None
        for candidate in ["Published_Date", "Event_Date", "event_date", "Date", "date"]:
            if candidate in df.columns:
                date_col = candidate
                break

        if date_col is None:
            print(f"  WARNING: no date column found in {name}")
            continue

        dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
        for d in dates:
            all_dates.append({"date": d, "source": name})

    if not all_dates:
        print("ERROR: no dated events loaded")
        return

    events = pd.DataFrame(all_dates)
    total = len(events)
    print(f"\nTotal dated events: {total}")

    # ---- 14-day periodicity test (chi-square) ----
    events["day_of_year"] = events["date"].dt.dayofyear
    events["bin_14"] = events["day_of_year"] % 14
    observed = events["bin_14"].value_counts().sort_index().values
    expected = np.full_like(observed, total / 14, dtype=float)
    chi2, p_chi2 = stats.chisquare(observed, f_exp=expected)
    print(f"\n14-day periodicity chi-square: χ² = {chi2:.2f}, p = {p_chi2:.6f}")

    # ---- December 2025 cluster ----
    dec_2025_start = pd.Timestamp("2025-12-05")
    dec_2025_end = pd.Timestamp("2026-01-02")
    dec_cluster = events[(events["date"] >= dec_2025_start) & (events["date"] <= dec_2025_end)]
    print(f"December 2025 cluster (±14-day window): {len(dec_cluster)} events")

    print("\nDataset breakdown in December 2025 window:")
    if len(dec_cluster) > 0:
        for src, cnt in dec_cluster["source"].value_counts().items():
            print(f"  {src}: {cnt}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("ORIGINAL ANALYSIS REPRODUCTION SUITE")
    print("Uses ONLY pre-2026 datasets (Control_Proof, Project_Trident, Silicon_Sovereignty)")
    print("New_Data_2026/ is explicitly EXCLUDED — those datasets were not part")
    print("of the original correlations.")
    print("=" * 80)

    part1_reflexive_control()
    part2_project_trident()
    part3_cross_validation()

    print("\n" + "=" * 80)
    print("ORIGINAL DATASETS USED IN THIS ANALYSIS")
    print("=" * 80)
    print("""
1. Control_Proof/master_reflexive_correlation_data.csv        (30 weeks, v3.1)
2. Control_Proof/reflexive_control_scraped_data.csv           (OSINT triggers, v3.1)
3. Project_Trident/Best_Data_For_Project_Trident/
     Lag_Correlation_Analysis_Verified_Holidays.csv           (533 records, v4.5)
4. 09_Silicon_Sovereignty/Coalition_Narrative_Map_2015-2025.csv   (456 records, v5.5)
5. 09_Silicon_Sovereignty/VOCA_funding_timeline_clean.csv         (667 records, v5.5)
6. 09_Silicon_Sovereignty/Regulatory_Map_Data_CLEANED.csv         (76 records, v5.5)
7. 09_Silicon_Sovereignty/REFINED_supercomputer_geopolitics (1).csv (906 records, v5.5)

NOT USED (New_Data_2026/ — intended for future analysis, not original correlations):
  - Additional_Anchors_Jan2026_Final.csv
  - Biopharma.csv
  - BlackRock_Timeline_Full_Decade.csv
  - CRINK_Intelligence_Dataset_Final_Verified.csv
  - High_Growth_Companies_2015_2026.csv
  - Infrastructure_Forensics.csv
  - Timeline_Update_Jan2026_Corrected (1).csv
""")
    print("=" * 80)
    print("END OF ORIGINAL ANALYSIS REPRODUCTION")
    print("=" * 80)
