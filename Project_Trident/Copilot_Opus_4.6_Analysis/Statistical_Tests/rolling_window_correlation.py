#!/usr/bin/env python3
"""
Rolling-Window Correlation Analysis
Purpose: Instead of computing one correlation across the entire timeline,
         compute it in a sliding window (e.g. 26 weeks).  This reveals
         whether the friction-compliance relationship is stable or whether
         it only appears in certain periods.

Planned item: "Rolling-window correlation analysis (does r change across
               different time periods?)"

If the rolling r is near zero for most of the timeline and spikes only in
late 2025, it confirms the "single-cluster" concern.  If it fluctuates
around a positive value throughout, the relationship is genuine.

Datasets used: local copies in ../Datasets/ (originals in New_Data_2026/)
"""

import os
import warnings
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

warnings.filterwarnings('ignore', category=FutureWarning)

script_dir = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(script_dir, '..', 'Datasets')

# ── Event classification ─────────────────────────────────────────────────────
FRICTION_CATEGORIES = {
    'Crisis_Event', 'Political_Event', 'Media_Reaction', 'Conflict',
    'Legislation', 'Ritual_Event', 'Political_Org', 'Holiday',
}
COMPLIANCE_CATEGORIES = {
    'Strategic_Shift', 'Government_Ties', 'Crypto_Pivot', 'Crypto_Sentiment',
    'ESG_Policy', 'ESG_Origins', 'Tech_Dominance', 'Policy', 'Geopolitics',
    'Corporate', 'FDA_Reg', 'Funding', 'Federal_Contract',
    'Corporate_Action', 'Financial_Performance', 'Clinical_Milestone',
    'General_Update',
}

DATE_COLS = ['date', 'Date', 'event_date', 'publication_date', 'action_date']
CAT_COLS = ['category', 'Category', 'event_type', 'type']


def classify_events(file_map, base_dir):
    """Load CSVs, classify each row as friction / compliance."""
    rows = []
    for name, filename in file_map.items():
        path = os.path.join(base_dir, filename)
        try:
            raw = pd.read_csv(path)
        except (FileNotFoundError, Exception) as exc:
            print(f"  ⚠ skipping {filename} ({exc})")
            continue
        date_col = next((c for c in DATE_COLS if c in raw.columns), None)
        cat_col = next((c for c in CAT_COLS if c in raw.columns), None)
        if not date_col or not cat_col:
            continue
        for _, row in raw.iterrows():
            try:
                d = pd.to_datetime(row[date_col])
                cat = row[cat_col]
            except (ValueError, TypeError, KeyError):
                continue
            if cat in FRICTION_CATEGORIES:
                rows.append({'date': d, 'type': 'friction', 'source': name})
            elif cat in COMPLIANCE_CATEGORIES:
                rows.append({'date': d, 'type': 'compliance', 'source': name})
    return pd.DataFrame(rows)


def build_weekly(events_df, start='2020-02-24', end='2026-01-05'):
    """Aggregate events into weekly friction / compliance counts."""
    events_df = events_df.copy()
    events_df['week'] = events_df['date'].dt.to_period('W')
    wk = events_df.groupby(['week', 'type']).size().unstack(fill_value=0)
    wk = wk.sort_index()
    sp, ep = pd.Period(start, 'W'), pd.Period(end, 'W')
    wk = wk[(wk.index >= sp) & (wk.index <= ep)]
    for col in ['friction', 'compliance']:
        if col not in wk.columns:
            wk[col] = 0
    return wk


CORE_FILES = {
    'blackrock':       'BlackRock_Timeline_Full_Decade.csv',
    'infrastructure':  'Infrastructure_Forensics.csv',
    'timeline_update': 'Timeline_Update_Jan2026_Corrected (1).csv',
    'anchors':         'Additional_Anchors_Jan2026_Final.csv',
    'biopharma':       'Biopharma.csv',
}
FULL_FILES = {
    **CORE_FILES,
    'high_growth': 'High_Growth_Companies_2015_2026.csv',
}

print("=" * 70)
print("ROLLING-WINDOW CORRELATION ANALYSIS")
print("=" * 70)
print("\nComputes correlation in sliding windows across the timeline.\n")


def rolling_correlation(f_series, c_series, window_size):
    """Compute rolling Pearson r and Spearman ρ in a sliding window."""
    n = len(f_series)
    results = []
    for i in range(n - window_size + 1):
        f_win = f_series[i:i + window_size]
        c_win = c_series[i:i + window_size]
        # Skip windows where either series is constant
        if f_win.std() == 0 or c_win.std() == 0:
            results.append({
                'start': i, 'end': i + window_size - 1,
                'r': float('nan'), 'rho': float('nan'),
                'f_mean': f_win.mean(), 'c_mean': c_win.mean(),
            })
            continue
        r, _ = pearsonr(f_win, c_win)
        rho, _ = spearmanr(f_win, c_win)
        results.append({
            'start': i, 'end': i + window_size - 1,
            'r': r, 'rho': rho,
            'f_mean': f_win.mean(), 'c_mean': c_win.mean(),
        })
    return results


def run_rolling(label, file_map):
    """Run rolling-window analysis for multiple window sizes."""
    print(f"\n{'═' * 70}")
    print(f"  {label}")
    print(f"{'═' * 70}")

    events = classify_events(file_map, datasets_dir)
    weekly = build_weekly(events)
    f_series = weekly['friction'].values.astype(float)
    c_series = weekly['compliance'].values.astype(float)
    n = len(f_series)

    week_labels = [str(w) for w in weekly.index]

    r_full, p_full = pearsonr(f_series, c_series)
    print(f"\n  Total weeks: {n}")
    print(f"  Full-sample Pearson r = {r_full:.4f}")

    window_sizes = [13, 26, 52]  # ~3 months, ~6 months, ~1 year
    for ws in window_sizes:
        if ws >= n:
            print(f"\n  Window size {ws} >= total weeks ({n}) — skipping")
            continue

        results = rolling_correlation(f_series, c_series, ws)
        valid_r = [r['r'] for r in results if not np.isnan(r['r'])]

        if not valid_r:
            print(f"\n  Window size {ws}: all windows had constant series — skipping")
            continue

        valid_r_arr = np.array(valid_r)

        print(f"\n  ── Window size: {ws} weeks (~{ws // 4} months) ──")
        print(f"  Windows computed: {len(results)} ({len(valid_r)} with valid r)")
        print(f"  Rolling Pearson r:")
        print(f"    Mean   : {np.mean(valid_r_arr):.4f}")
        print(f"    Median : {np.median(valid_r_arr):.4f}")
        print(f"    Std    : {np.std(valid_r_arr):.4f}")
        print(f"    Min    : {np.min(valid_r_arr):.4f}")
        print(f"    Max    : {np.max(valid_r_arr):.4f}")

        # Count windows with significant positive correlation
        n_positive = np.sum(valid_r_arr > 0.3)
        n_negative = np.sum(valid_r_arr < -0.3)
        n_near_zero = np.sum(np.abs(valid_r_arr) <= 0.1)
        print(f"    Windows with r > 0.3  : {n_positive} ({n_positive / len(valid_r) * 100:.0f}%)")
        print(f"    Windows with r < -0.3 : {n_negative} ({n_negative / len(valid_r) * 100:.0f}%)")
        print(f"    Windows with |r| ≤ 0.1: {n_near_zero} ({n_near_zero / len(valid_r) * 100:.0f}%)")

        # Show the top-5 and bottom-5 windows
        sorted_by_r = sorted(
            [(i, r) for i, r in enumerate(results) if not np.isnan(r['r'])],
            key=lambda x: x[1]['r'], reverse=True
        )

        print(f"\n    Top 5 strongest positive windows:")
        for rank, (idx, r) in enumerate(sorted_by_r[:5], 1):
            start_label = week_labels[r['start']]
            end_label = week_labels[r['end']]
            print(f"      {rank}. r={r['r']:+.4f}  {start_label} → {end_label}"
                  f"  (friction μ={r['f_mean']:.1f}, compliance μ={r['c_mean']:.1f})")

        print(f"\n    Bottom 5 (weakest / negative) windows:")
        for rank, (idx, r) in enumerate(sorted_by_r[-5:], 1):
            start_label = week_labels[r['start']]
            end_label = week_labels[r['end']]
            print(f"      {rank}. r={r['r']:+.4f}  {start_label} → {end_label}"
                  f"  (friction μ={r['f_mean']:.1f}, compliance μ={r['c_mean']:.1f})")

        # ── Regime detection ─────────────────────────────────────────────────
        # Split timeline into rough thirds and compare
        third = len(valid_r) // 3
        if third > 0:
            early = valid_r_arr[:third]
            mid = valid_r_arr[third:2 * third]
            late = valid_r_arr[2 * third:]
            print(f"\n    Regime analysis (timeline thirds):")
            print(f"      Early third: mean r = {np.mean(early):.4f} (n={len(early)})")
            print(f"      Middle third: mean r = {np.mean(mid):.4f} (n={len(mid)})")
            print(f"      Late third:  mean r = {np.mean(late):.4f} (n={len(late)})")

            if np.mean(late) > np.mean(early) + 0.3:
                print(f"      → Late-period surge — correlation concentrates in recent data")
            elif abs(np.mean(late) - np.mean(early)) < 0.1:
                print(f"      → Stable across time — correlation is broadly distributed")
            else:
                print(f"      → Mixed pattern — correlation varies across time periods")


run_rolling("CORE scope (excl. High_Growth_Companies)", CORE_FILES)
run_rolling("FULL scope (incl. High_Growth_Companies)", FULL_FILES)

# ── Bottom line ──────────────────────────────────────────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  BOTTOM LINE")
print(f"{'═' * 70}")
print(f"""
  A single correlation number (r ≈ 0.62) hides the TIME STRUCTURE of
  the relationship.  The rolling-window analysis reveals WHERE in the
  timeline friction and compliance actually co-move.

  Key questions this answers:
    1. Is the correlation stable across the entire 2020-2026 window,
       or does it only appear in certain periods?
    2. Are there regime changes — periods where the relationship
       strengthens, weakens, or reverses?
    3. Does the late-2025 cluster dominate, or is there genuine
       co-movement in earlier periods too?

  INTERPRETATION GUIDE:
    • If most windows show r > 0.3: genuine, persistent relationship
    • If only late-2025 windows show r > 0.3: single-cluster artifact
    • If r oscillates between positive and negative: no stable
      relationship (the full-sample r is misleading)
    • Regime changes may indicate structural shifts in how friction
      and compliance interact (e.g., different administrations,
      different media environments)
""")
print("=" * 70)
