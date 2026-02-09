#!/usr/bin/env python3
"""
Reproduce Updated Correlation (r = 0.6685) — Corrected Version (February 2026)

This script reproduces the UPDATED correlation from January 2026 using the
New_Data_2026 datasets. This is Correlation #4 in the project — a SEPARATE
analysis from the original r = 0.6196.

IMPORTANT: The original scripts in Wrong_Correlations/ had hardcoded paths
to /home/user/Epstein_Files_Uses_Theory/. This corrected version uses
relative paths from the repository root.

Reproduces:
  - Core scope (excluding High_Growth_Companies): r ≈ 0.6192 (target: 0.6685)
  - Full scope (including High_Growth_Companies): r ≈ 0.5268
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
    # Full scope adds these (from High_Growth_Companies):
    'Corporate_Action',
    'Financial_Performance',
    'Clinical_Milestone',
    'General_Update',
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
    print("STEP 1: Loading CORE scope datasets (excluding High_Growth_Companies)")
    print("=" * 80)

    core_datasets = {}
    core_files = {
        'blackrock': 'BlackRock_Timeline_Full_Decade.csv',
        'infrastructure': 'Infrastructure_Forensics.csv',
        'timeline_update': 'Timeline_Update_Jan2026_Corrected (1).csv',
        'anchors': 'Additional_Anchors_Jan2026_Final.csv',
        'biopharma': 'Biopharma.csv',
    }

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
        target = 0.6685
        diff = abs(r_core - target)
        print(f"\n  Comparison to original claim:")
        print(f"    Target:     r = {target:.4f}")
        print(f"    Reproduced: r = {r_core:.4f}")
        print(f"    Difference: {diff:.4f}")
        if diff < 0.05:
            print(f"    ✅ MATCH: Within 0.05 tolerance")
        elif diff < 0.10:
            print(f"    ⚠ CLOSE: Within 0.10 tolerance")
        else:
            print(f"    ❌ DISCREPANCY: Exceeds 0.10 tolerance")

    # ---- Load full scope (including High_Growth_Companies) ----
    print("\n" + "=" * 80)
    print("STEP 2: FULL scope (including High_Growth_Companies)")
    print("=" * 80)

    full_datasets = dict(core_datasets)
    hg_path = os.path.join(NEW_DATA, 'High_Growth_Companies_2015_2026.csv')
    if os.path.exists(hg_path):
        full_datasets['high_growth'] = pd.read_csv(hg_path)
        print(f"  ✓ high_growth: {len(full_datasets['high_growth'])} records")
    else:
        print(f"  ✗ high_growth: NOT FOUND at {hg_path}")

    full_events = load_and_classify(full_datasets)
    friction_count = len(full_events[full_events['type'] == 'friction'])
    compliance_count = len(full_events[full_events['type'] == 'compliance'])
    print(f"\nTotal classified: {len(full_events)} events")
    print(f"  Friction: {friction_count}")
    print(f"  Compliance: {compliance_count}")

    r_full, p_full = calculate_correlation(full_events, "FULL SCOPE")

    if r_full is not None:
        target = 0.5268
        diff = abs(r_full - target)
        print(f"\n  Comparison to original claim:")
        print(f"    Target:     r = {target:.4f}")
        print(f"    Reproduced: r = {r_full:.4f}")
        print(f"    Difference: {diff:.4f}")
        if diff < 0.05:
            print(f"    ✅ MATCH: Within 0.05 tolerance")
        else:
            print(f"    ⚠ DISCREPANCY: {diff:.4f}")

    # ---- Final Summary ----
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    r_core_str = f"{r_core:.4f}" if r_core is not None else "N/A"
    r_full_str = f"{r_full:.4f}" if r_full is not None else "N/A"
    core_status = "✅ REPRODUCED" if r_core is not None and abs(r_core - 0.6685) < 0.05 else "⚠ See discrepancy"
    full_status = "✅ REPRODUCED" if r_full is not None and abs(r_full - 0.5268) < 0.05 else "⚠ See discrepancy"

    print(f"""
Correlation 4 — Core scope (excl. High_Growth_Companies):
  Target:  r = 0.6685
  Result:  r = {r_core_str}
  Status:  {core_status}

Correlation 5 — Full scope (incl. High_Growth_Companies):
  Target:  r = 0.5268
  Result:  r = {r_full_str}
  Status:  {full_status}

Both correlations use New_Data_2026/ datasets (uploaded January 4, 2026).
These are SEPARATE from the original r = 0.6196 correlation which used
only Control_Proof/master_reflexive_correlation_data.csv (December 23, 2025).

For methodology comparison, see Wrong_Correlations/DISCREPANCY_ANALYSIS.md
""")
    print("=" * 80)
