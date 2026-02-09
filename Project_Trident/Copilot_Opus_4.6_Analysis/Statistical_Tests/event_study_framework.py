#!/usr/bin/env python3
"""
Event-Study Framework
Purpose: Instead of correlating aggregate weekly counts, this analysis
         centers on individual friction events and measures whether
         compliance events cluster in a defined window AFTER each
         friction event.

Planned item: "Event-study framework (measure compliance response in a
               defined window around each friction event)"

This is the most granular test: for each friction event, count how many
compliance events occur in the next 1, 7, 14, and 28 days, then compare
to a baseline rate.  If compliance genuinely responds to friction, the
post-friction window should have significantly more compliance events
than random windows of the same length.

Datasets used: original pre-2026 datasets (Control_Proof, Project_Trident,
               Silicon_Sovereignty)
"""

import os
import warnings
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu, ttest_ind

from original_data_loader import load_friction_events, load_compliance_events, build_weekly_counts, REPO_ROOT

warnings.filterwarnings('ignore', category=FutureWarning)

SEED = 42
rng = np.random.default_rng(SEED)

print("=" * 70)
print("EVENT-STUDY FRAMEWORK")
print("=" * 70)
print("\nMeasures compliance response in defined windows around friction events.")
print("Datasets: original pre-2026 (Control_Proof, Project_Trident, Silicon_Sovereignty)\n")

friction_events = load_friction_events()
compliance_events = load_compliance_events()

if friction_events.empty or compliance_events.empty:
    print("  Insufficient events for analysis.")
    exit(0)

friction_dates = friction_events['date'].sort_values().values
compliance_dates = compliance_events['date'].sort_values().values

print(f"\n  Friction events:   {len(friction_dates)}")
print(f"  Compliance events: {len(compliance_dates)}")

# Convert to numpy datetime64 for fast computation
f_dates_ns = friction_dates.astype('datetime64[ns]')
c_dates_ns = compliance_dates.astype('datetime64[ns]')

# ── For each friction event, count compliance in post-event windows ──────
windows = [1, 7, 14, 28]
post_counts = {w: [] for w in windows}
pre_counts = {w: [] for w in windows}  # control: same window BEFORE

for f_date in f_dates_ns:
    for w in windows:
        # Post-friction window: [f_date, f_date + w days)
        window_start = f_date
        window_end = f_date + np.timedelta64(w, 'D')
        post_n = np.sum((c_dates_ns >= window_start) & (c_dates_ns < window_end))
        post_counts[w].append(int(post_n))

        # Pre-friction window: [f_date - w days, f_date)
        pre_start = f_date - np.timedelta64(w, 'D')
        pre_end = f_date
        pre_n = np.sum((c_dates_ns >= pre_start) & (c_dates_ns < pre_end))
        pre_counts[w].append(int(pre_n))

# ── Results per window ───────────────────────────────────────────────────
print(f"\n  ── Compliance Events in Post-Friction Windows ──")
print(f"  {'Window':>10} {'Post-mean':>10} {'Pre-mean':>10} {'Ratio':>8} "
      f"{'Mann-W p':>10} {'t-test p':>10}")
print(f"  {'─' * 58}")

study_results = []
for w in windows:
    post = np.array(post_counts[w])
    pre = np.array(pre_counts[w])
    post_mean = np.mean(post)
    pre_mean = np.mean(pre)
    ratio = post_mean / pre_mean if pre_mean > 0 else float('inf')

    try:
        u_stat, u_p = mannwhitneyu(post, pre, alternative='greater')
    except ValueError:
        u_p = 1.0

    try:
        t_stat, t_p = ttest_ind(post, pre, alternative='greater')
    except Exception:
        t_p = 1.0

    print(f"  {w:>8}d {post_mean:>10.2f} {pre_mean:>10.2f} {ratio:>8.2f}x "
          f"{u_p:>10.4f} {t_p:>10.4f}")

    study_results.append({
        'window': w, 'post_mean': post_mean, 'pre_mean': pre_mean,
        'ratio': ratio, 'u_p': u_p, 't_p': t_p,
    })

# ── Random-baseline comparison ───────────────────────────────────────────
print(f"\n  ── Random Baseline Comparison (1,000 random dates) ──")

date_range_start = np.nanmin(np.concatenate([f_dates_ns, c_dates_ns]))
date_range_end = np.nanmax(np.concatenate([f_dates_ns, c_dates_ns]))
td = date_range_end - date_range_start
range_days = int(td / np.timedelta64(1, 'D'))

if range_days <= 0:
    print("  ⚠ Date range is zero or negative — skipping random baseline")
else:
    N_RANDOM = 1000
    random_counts = {w: [] for w in windows}
    for _ in range(N_RANDOM):
        rand_offset = rng.integers(0, max(range_days, 1))
        rand_date = date_range_start + np.timedelta64(rand_offset, 'D')
        for w in windows:
            window_end = rand_date + np.timedelta64(w, 'D')
            n_rand = int(np.sum((c_dates_ns >= rand_date) & (c_dates_ns < window_end)))
            random_counts[w].append(n_rand)

    print(f"  {'Window':>10} {'Actual':>10} {'Random':>10} {'Ratio':>8} {'p (> random)':>14}")
    print(f"  {'─' * 52}")
    for w in windows:
        actual_mean = np.mean(post_counts[w])
        random_mean = np.mean(random_counts[w])
        ratio = actual_mean / random_mean if random_mean > 0 else float('inf')
        exceed = np.mean(np.array(random_counts[w]) >= actual_mean)
        print(f"  {w:>8}d {actual_mean:>10.2f} {random_mean:>10.2f} {ratio:>8.2f}x "
              f"{exceed:>14.4f}")

# ── Per-source breakdown ─────────────────────────────────────────────────
print(f"\n  ── Top Friction Sources Driving Compliance Response ──")
friction_sources = friction_events['source'].value_counts()
print(f"  Friction source distribution:")
for src, cnt in friction_sources.items():
    print(f"    {src}: {cnt} events")

# For the 14-day window, break down by friction source
if len(friction_events) > 0:
    print(f"\n  14-day post-event compliance (by friction source):")
    for src in friction_sources.index[:5]:
        src_dates = friction_events[friction_events['source'] == src]['date'].values
        src_dates_ns = src_dates.astype('datetime64[ns]')
        counts_14 = []
        for fd in src_dates_ns:
            n_c = int(np.sum(
                (c_dates_ns >= fd) & (c_dates_ns < fd + np.timedelta64(14, 'D'))
            ))
            counts_14.append(n_c)
        mean_14 = np.mean(counts_14) if counts_14 else 0
        print(f"    {src}: mean = {mean_14:.1f} compliance events in 14d window "
              f"(n={len(src_dates)} friction events)")

# ── Interpretation ───────────────────────────────────────────────────────
print(f"\n  ── Interpretation ──")
w14 = next((r for r in study_results if r['window'] == 14), None)
if w14:
    if w14['u_p'] < 0.05 and w14['ratio'] > 1.5:
        print(f"  ✓ SIGNIFICANT compliance clustering after friction events")
        print(f"    14-day window: {w14['ratio']:.1f}x more compliance events after")
        print(f"    friction than before (p={w14['u_p']:.4f})")
        print(f"    This supports the 'friction triggers compliance' hypothesis.")
    elif w14['u_p'] < 0.05:
        print(f"  ⚠ Statistically significant but weak effect (ratio={w14['ratio']:.2f}x)")
        print(f"    The difference is real but small.")
    else:
        print(f"  ✗ No significant compliance clustering after friction events")
        print(f"    14-day window: ratio={w14['ratio']:.2f}x, p={w14['u_p']:.4f}")
        print(f"    Compliance events are not systematically triggered by friction.")

# ── Bottom line ──────────────────────────────────────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  BOTTOM LINE")
print(f"{'═' * 70}")
print(f"""
  Original pre-2026 datasets (Control_Proof, Project_Trident,
  Silicon_Sovereignty) — {len(friction_dates)} friction events,
  {len(compliance_dates)} compliance events.

  The event-study framework is the most granular test in this suite.
  Instead of asking "do weekly aggregate counts move together?" it asks
  "when a specific friction event occurs, does compliance follow?"

  This is important because aggregate correlation can be an artifact of
  shared density (both types of events happen more in busy months),
  while event-level analysis tests the DIRECTIONAL MECHANISM:

    Friction event → [delay] → Compliance response

  Three tests are run:
    1. PRE vs POST: Do more compliance events occur AFTER a friction
       event than BEFORE it?  (Mann-Whitney U test)
    2. ACTUAL vs RANDOM: Do friction events attract more compliance
       than random dates would?  (Monte Carlo baseline)
    3. SOURCE BREAKDOWN: Which sources of friction events most
       strongly predict compliance responses?

  If the event-study finds significance, it's stronger evidence for a
  causal mechanism than aggregate correlation.  If it doesn't, the
  aggregate r may just reflect shared seasonality or density patterns.
""")
print("=" * 70)
