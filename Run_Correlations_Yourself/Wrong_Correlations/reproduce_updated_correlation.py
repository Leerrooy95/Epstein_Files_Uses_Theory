#!/usr/bin/env python3
"""
Reproduce Updated Correlation — Corrected Version (February 2026)

This script reproduces the UPDATED correlation from January 2026 using the
New_Data_2026 datasets. This is Correlation #4 in the project — a SEPARATE
analysis from the original r = 0.6196.

IMPORTANT: The original scripts in Wrong_Correlations/ had hardcoded paths
to /home/user/Epstein_Files_Uses_Theory/. This corrected version uses
relative paths from the repository root.

IMPORTANT: Datasets covering only 2025(-2026) data are EXCLUDED because
narrow time windows inflate correlations. Excluded files:
  - Infrastructure_Forensics.csv          (2025 only)
  - Timeline_Update_Jan2026_Corrected (1).csv  (2025-2026 only)
  - Additional_Anchors_Jan2026_Final.csv  (2025-2026 only)

IMPORTANT: High_Growth_Companies_2015_2026.csv is also EXCLUDED because the
scraping methodology needs to be redone before it can be trusted for
correlation analysis.

Uses:
  - BlackRock_Timeline_Full_Decade.csv (2015-2026)
  - Biopharma.csv (2023-2026)
"""

import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

# ---------------------------------------------------------------------------
# Resolve paths relative to this script → repository root
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
NEW_DATA = os.path.join(REPO_ROOT, "New_Data_2026")


# ============================================================================
# Event classification categories (from original 2026_Analysis.md)
# ============================================================================

FRICTION_CATEGORIES = [
    'Crisis_Event',
    'Political_Event',
    'Media_Reaction',
    'Conflict',
    'Legislation',
    'Ritual_Event',
    'Political_Org',
    'Holiday',
]

COMPLIANCE_CATEGORIES = [
    'Strategic_Shift',
    'Government_Ties',
    'Crypto_Pivot',
    'Crypto_Sentiment',
    'ESG_Policy',
    'ESG_Origins',
    'Tech_Dominance',
    'Policy',
    'Geopolitics',
    'Corporate',
    'FDA_Reg',
    'Funding',
    'Federal_Contract',
]


def load_and_classify(datasets):
    """Load datasets and classify events as friction or compliance."""
    all_events = []

    for name, df in datasets.items():
        date_col = None
        for col in ['date', 'Date', 'event_date', 'publication_date', 'action_date']:
            if col in df.columns:
                date_col = col
                break

        cat_col = None
        for col in ['category', 'Category', 'event_type', 'type']:
            if col in df.columns:
                cat_col = col
                break

        if date_col and cat_col:
            for _, row in df.iterrows():
                try:
                    event_date = pd.to_datetime(row[date_col])
                    category = row[cat_col]

                    event_type = None
                    if category in FRICTION_CATEGORIES:
                        event_type = 'friction'
                    elif category in COMPLIANCE_CATEGORIES:
                        event_type = 'compliance'

                    if event_type:
                        all_events.append({
                            'date': event_date,
                            'type': event_type,
                            'category': category,
                            'source': name
                        })
                except Exception:
                    continue

    return pd.DataFrame(all_events)


def calculate_correlation(events_df, label=""):
    """Calculate Pearson and Spearman correlation from event DataFrame."""
    events_df = events_df.copy()
    events_df['week'] = events_df['date'].dt.to_period('W')
    weekly_counts = events_df.groupby(['week', 'type']).size().unstack(fill_value=0)
    weekly_counts = weekly_counts.sort_index()

    # Filter to analysis period
    start_period = pd.Period('2020-02-24', 'W')
    end_period = pd.Period('2026-01-05', 'W')
    weekly_counts = weekly_counts[
        (weekly_counts.index >= start_period) & (weekly_counts.index <= end_period)
    ]

    if 'friction' not in weekly_counts.columns or 'compliance' not in weekly_counts.columns:
        print(f"  ⚠ Could not calculate correlation — missing data columns")
        return None, None

    friction_series = weekly_counts['friction']
    compliance_series = weekly_counts['compliance']

    r, p = pearsonr(friction_series, compliance_series)
    rho, p_spearman = spearmanr(friction_series, compliance_series)

    print(f"\n{label} Results:")
    print(f"  Weekly time series: {len(weekly_counts)} weeks")
    print(f"  Pearson r (0-lag):  {r:.4f}, p = {p:.6f}")
    print(f"  Spearman ρ (0-lag): {rho:.4f}, p = {p_spearman:.6f}")

    # Lag analysis
    print(f"\n  Lag correlation comparison:")
    print(f"  {'Lag':<10} {'Pearson r':<15} {'p-value':<15}")
    print(f"  {'-'*40}")
    for lag in [0, 1, 2, 3, 4]:
        if lag == 0:
            r_lag, p_lag = pearsonr(friction_series, compliance_series)
        else:
            lagged = friction_series.shift(lag)
            valid_idx = ~lagged.isna()
            if valid_idx.sum() > 2:
                r_lag, p_lag = pearsonr(lagged[valid_idx], compliance_series[valid_idx])
            else:
                r_lag, p_lag = float('nan'), float('nan')
        print(f"  {lag:<10} {r_lag:<15.4f} {p_lag:<15.6f}")

    return r, p


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UPDATED CORRELATION REPRODUCTION — CORRECTED VERSION")
    print("Uses New_Data_2026/ datasets with correct relative paths")
    print("=" * 80)

    # ---- Load core scope datasets (excluding High_Growth_Companies) ----
    print("\n" + "=" * 80)
    print("STEP 1: Loading datasets (BlackRock + Biopharma)")
    print("=" * 80)

    core_datasets = {}
    core_files = {
        'blackrock': 'BlackRock_Timeline_Full_Decade.csv',
        'biopharma': 'Biopharma.csv',
    }

    # NOTE: The following datasets are EXCLUDED from correlation analysis
    # because they contain only 2025(-2026) data, which inflates the
    # correlation by concentrating events in a narrow time window:
    #   - Infrastructure_Forensics.csv          (2025 only, 107 rows)
    #   - Timeline_Update_Jan2026_Corrected (1).csv  (2025-2026 only, 99 rows)
    #   - Additional_Anchors_Jan2026_Final.csv  (2025-2026 only, 50 rows)

    for name, filename in core_files.items():
        path = os.path.join(NEW_DATA, filename)
        if os.path.exists(path):
            core_datasets[name] = pd.read_csv(path)
            print(f"  ✓ {name}: {len(core_datasets[name])} records")
        else:
            print(f"  ✗ {name}: NOT FOUND at {path}")

    core_events = load_and_classify(core_datasets)
    friction_count = len(core_events[core_events['type'] == 'friction'])
    compliance_count = len(core_events[core_events['type'] == 'compliance'])
    print(f"\nTotal classified: {len(core_events)} events")
    print(f"  Friction: {friction_count}")
    print(f"  Compliance: {compliance_count}")

    print("\nBreakdown by dataset:")
    for source in core_events['source'].unique():
        source_df = core_events[core_events['source'] == source]
        f = len(source_df[source_df['type'] == 'friction'])
        c = len(source_df[source_df['type'] == 'compliance'])
        print(f"  {source}: {f} friction, {c} compliance")

    r_core, p_core = calculate_correlation(core_events, "CORE SCOPE")

    if r_core is not None:
        print(f"\n  Note: The previously reported r = 0.6685 included 2025-only")
        print(f"  datasets that have been excluded. The current result reflects")
        print(f"  only multi-year datasets (BlackRock, Biopharma).")

    # ---- Final Summary ----
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    r_core_str = f"{r_core:.4f}" if r_core is not None else "N/A"

    print(f"""
Updated correlation (BlackRock + Biopharma only):
  Previous (with 2025-only datasets):  r = 0.6685
  Current  (multi-year datasets only): r = {r_core_str}

Excluded datasets:
  - Infrastructure_Forensics.csv          (2025 only, 107 rows)
  - Timeline_Update_Jan2026_Corrected (1).csv  (2025-2026 only, 99 rows)
  - Additional_Anchors_Jan2026_Final.csv  (2025-2026 only, 50 rows)
  - High_Growth_Companies_2015_2026.csv   (scraping methodology needs redo)

Both correlations use New_Data_2026/ datasets (uploaded January 4, 2026).
These are SEPARATE from the original r = 0.6196 correlation which used
only Control_Proof/master_reflexive_correlation_data.csv (December 23, 2025).

For methodology comparison, see Wrong_Correlations/DISCREPANCY_ANALYSIS.md
""")
    print("=" * 80)
