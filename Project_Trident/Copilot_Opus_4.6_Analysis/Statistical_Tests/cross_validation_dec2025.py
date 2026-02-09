#!/usr/bin/env python3
"""
Cross-Validation: Does the Pattern Hold When December 2025 Is Excluded?
Purpose: December 2025 is the densest month in the dataset — dozens of events
         cluster in a ~3-week window.  This script removes Dec 2025 entirely
         and checks whether the friction-compliance correlation survives.

Planned item: "Cross-validation: does the pattern hold when Dec 2025 is excluded?"

If the correlation drops to near zero without Dec 2025, then the entire
result is driven by a single month.  If it remains significant,
the pattern is genuine across the broader timeline.

Datasets used: original pre-2026 datasets (Control_Proof, Project_Trident,
               Silicon_Sovereignty)
"""

import os
import warnings
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

from original_data_loader import load_friction_events, load_compliance_events, build_weekly_counts, REPO_ROOT

warnings.filterwarnings('ignore', category=FutureWarning)

print("=" * 70)
print("CROSS-VALIDATION: EXCLUDING DECEMBER 2025")
print("=" * 70)
print("\nTests whether the friction-compliance correlation survives when the")
print("densest month (Dec 2025) is removed entirely.")
print("Datasets: original pre-2026 (Control_Proof, Project_Trident, Silicon_Sovereignty)\n")

friction_events = load_friction_events()
compliance_events = load_compliance_events()
weekly_full = build_weekly_counts(friction_events, compliance_events)
f_full = weekly_full['friction'].values.astype(float)
c_full = weekly_full['compliance'].values.astype(float)
n_full = len(f_full)

r_full, p_full = pearsonr(f_full, c_full)
rho_full, p_rho_full = spearmanr(f_full, c_full)
print(f"\n  Full dataset: {n_full} weeks")
print(f"  Pearson  r = {r_full:.4f} (p={p_full:.6f})")
print(f"  Spearman ρ = {rho_full:.4f} (p={p_rho_full:.6f})")

# ── Exclusion tests ──────────────────────────────────────────────────────
# Each filter_fn receives a pandas Period object (weekly frequency).
# w.start_time returns the Timestamp of the period's start.
exclusions = {
    'Dec 2025 excluded': lambda w: not (w.start_time.year == 2025 and w.start_time.month == 12),
    'Nov-Dec 2025 excluded': lambda w: not (w.start_time.year == 2025 and w.start_time.month in [11, 12]),
    'Oct-Dec 2025 excluded': lambda w: not (w.start_time.year == 2025 and w.start_time.month in [10, 11, 12]),
    'All 2025 excluded': lambda w: w.start_time.year != 2025,
    'Only 2025': lambda w: w.start_time.year == 2025,
    'Only pre-2025': lambda w: w.start_time.year < 2025,
}

results = []
for name, filter_fn in exclusions.items():
    mask = [filter_fn(w) for w in weekly_full.index]
    f_sub = f_full[mask]
    c_sub = c_full[mask]
    n_sub = len(f_sub)

    if n_sub < 5:
        print(f"\n  {name}: only {n_sub} weeks — skipping")
        continue

    # Check if either series is constant (all zeros)
    if f_sub.std() == 0 or c_sub.std() == 0:
        print(f"\n  {name}: {n_sub} weeks — one series is constant (all zeros)")
        results.append({
            'name': name, 'n': n_sub,
            'r': float('nan'), 'p_r': float('nan'),
            'rho': float('nan'), 'p_rho': float('nan'),
        })
        continue

    r_sub, p_sub = pearsonr(f_sub, c_sub)
    rho_sub, p_rho_sub = spearmanr(f_sub, c_sub)

    # Count events in subset
    n_f = int(f_sub.sum())
    n_c = int(c_sub.sum())

    results.append({
        'name': name, 'n': n_sub,
        'r': r_sub, 'p_r': p_sub,
        'rho': rho_sub, 'p_rho': p_rho_sub,
        'n_friction': n_f, 'n_compliance': n_c,
    })

# ── Summary table ────────────────────────────────────────────────────────
print(f"\n  ── Cross-Validation Results ──")
print(f"  {'Window':<30} {'Weeks':>6} {'Pearson r':>10} {'p':>10} {'Spearman ρ':>11} {'p':>10}")
print(f"  {'─' * 77}")
print(f"  {'Full dataset':<30} {n_full:>6} {r_full:>10.4f} {p_full:>10.6f} {rho_full:>11.4f} {p_rho_full:>10.6f}")
for r in results:
    if np.isnan(r['r']):
        print(f"  {r['name']:<30} {r['n']:>6} {'N/A':>10} {'N/A':>10} {'N/A':>11} {'N/A':>10}")
    else:
        print(f"  {r['name']:<30} {r['n']:>6} {r['r']:>10.4f} {r['p_r']:>10.6f} {r['rho']:>11.4f} {r['p_rho']:>10.6f}")

# ── Interpretation ───────────────────────────────────────────────────────
dec_result = next((r for r in results if r['name'] == 'Dec 2025 excluded'), None)
pre_result = next((r for r in results if r['name'] == 'Only pre-2025'), None)

if dec_result and not np.isnan(dec_result['r']):
    print(f"\n  ── Interpretation ──")
    drop = r_full - dec_result['r']
    pct_drop = (drop / r_full) * 100 if r_full != 0 else 0
    print(f"  Removing Dec 2025: r drops from {r_full:.4f} → {dec_result['r']:.4f} "
          f"({pct_drop:.0f}% reduction)")

    if dec_result['p_r'] < 0.05:
        print(f"  ✓ Correlation SURVIVES Dec 2025 removal (p={dec_result['p_r']:.6f})")
        if pct_drop > 50:
            print(f"    However, the {pct_drop:.0f}% drop shows Dec 2025 is the dominant driver.")
        else:
            print(f"    The correlation is broadly distributed across the timeline.")
    else:
        print(f"  ✗ Correlation DOES NOT SURVIVE Dec 2025 removal (p={dec_result['p_r']:.6f})")
        print(f"    The entire r ≈ {r_full:.2f} result is driven by December 2025.")

if pre_result and not np.isnan(pre_result['r']):
    print(f"\n  Pre-2025 only: r = {pre_result['r']:.4f} (p={pre_result['p_r']:.6f})")
    if pre_result['p_r'] < 0.05:
        print(f"  ✓ Signal exists even in the pre-2025 data alone.")
    else:
        print(f"  ✗ No signal in pre-2025 data — the pattern is 2025-specific.")

# ── Bottom line ──────────────────────────────────────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  BOTTOM LINE")
print(f"{'═' * 70}")
print(f"""
  Original pre-2026 datasets (Control_Proof, Project_Trident,
  Silicon_Sovereignty) — {n_full} weekly bins.

  This test asks the most direct question about the correlation's validity:
  Is the friction-compliance co-movement a broad pattern, or is it entirely
  driven by the dense December 2025 cluster?

  If removing a single month destroys the correlation, the headline
  number is misleading — it describes one anomalous month,
  not a persistent relationship across the timeline.

  This is NOT a criticism of the data — December 2025 genuinely had
  extraordinary events.  But a robust correlation should not depend on
  any single time window.

  WHAT TO DO IF THE CORRELATION DROPS:
    1. Report the Dec-excluded r alongside the full r in any summary
    2. Focus analysis on WHY December 2025 is special (event-study
       framework) rather than claiming a broad time-series pattern
    3. Backfill earlier years (see backfill_guide.md) to build a
       dataset where no single month dominates
""")
print("=" * 70)
