#!/usr/bin/env python3
"""
Granger Causality Test
Purpose: Test whether friction event counts GRANGER-CAUSE compliance event
         counts (or vice versa).  Granger causality asks: "does knowing past
         friction values improve our ability to predict current compliance
         values, beyond what past compliance values alone provide?"

This is the most direct test of the temporal mechanism hypothesis:
    Friction(t-k) → Compliance(t)

If friction Granger-causes compliance, past friction contains predictive
information about future compliance.  If the reverse also holds, the
relationship is bidirectional (both react to a common driver).

Recommended in README.md as a planned technique ("Granger causality").

Datasets used: original pre-2026 datasets (Control_Proof, Project_Trident,
               Silicon_Sovereignty)
"""

import os
import warnings
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

from original_data_loader import load_friction_events, load_compliance_events, build_weekly_counts, REPO_ROOT

warnings.filterwarnings('ignore', category=FutureWarning)

print("=" * 70)
print("GRANGER CAUSALITY TEST")
print("=" * 70)
print("\nTests whether past friction predicts future compliance (or vice versa).")
print("Uses the statsmodels Granger causality implementation.")
print("Datasets: original pre-2026 (Control_Proof, Project_Trident, Silicon_Sovereignty)\n")

friction_events = load_friction_events()
compliance_events = load_compliance_events()
weekly = build_weekly_counts(friction_events, compliance_events)
f_series = weekly['friction'].values.astype(float)
c_series = weekly['compliance'].values.astype(float)
n = len(f_series)

r_obs, p_obs = pearsonr(f_series, c_series)
print(f"\n  Weeks: {n}")
print(f"  Observed Pearson r = {r_obs:.4f} (p={p_obs:.6f})")

# ── Granger causality test ───────────────────────────────────────────────
from statsmodels.tsa.stattools import grangercausalitytests

data = pd.DataFrame({'compliance': c_series, 'friction': f_series})
max_lag = 8  # test lags 1-8 weeks

# ── Direction 1: Does friction Granger-cause compliance? ─────────────────
print(f"\n  ── Direction 1: Friction → Compliance ──")
print(f"  (Does past friction help predict current compliance?)")
print(f"\n  {'Lag (weeks)':>12} {'F-statistic':>14} {'p-value':>10} {'Significant?':>14}")
print(f"  {'─' * 50}")

try:
    gc_fc = grangercausalitytests(data[['compliance', 'friction']], maxlag=max_lag,
                                   verbose=False)
    fc_results = []
    for lag in range(1, max_lag + 1):
        f_stat = gc_fc[lag][0]['ssr_ftest'][0]
        p_val = gc_fc[lag][0]['ssr_ftest'][1]
        sig = "✓ Yes" if p_val < 0.05 else "✗ No"
        print(f"  {lag:>12} {f_stat:>14.4f} {p_val:>10.4f} {sig:>14}")
        fc_results.append({'lag': lag, 'f_stat': f_stat, 'p': p_val})
except Exception as exc:
    print(f"  Error: {exc}")
    fc_results = []

# ── Direction 2: Does compliance Granger-cause friction? ─────────────────
print(f"\n  ── Direction 2: Compliance → Friction ──")
print(f"  (Does past compliance help predict current friction?)")
print(f"\n  {'Lag (weeks)':>12} {'F-statistic':>14} {'p-value':>10} {'Significant?':>14}")
print(f"  {'─' * 50}")

try:
    gc_cf = grangercausalitytests(data[['friction', 'compliance']], maxlag=max_lag,
                                   verbose=False)
    cf_results = []
    for lag in range(1, max_lag + 1):
        f_stat = gc_cf[lag][0]['ssr_ftest'][0]
        p_val = gc_cf[lag][0]['ssr_ftest'][1]
        sig = "✓ Yes" if p_val < 0.05 else "✗ No"
        print(f"  {lag:>12} {f_stat:>14.4f} {p_val:>10.4f} {sig:>14}")
        cf_results.append({'lag': lag, 'f_stat': f_stat, 'p': p_val})
except Exception as exc:
    print(f"  Error: {exc}")
    cf_results = []

# ── Interpretation ───────────────────────────────────────────────────────
print(f"\n  ── Interpretation ──")

fc_sig = [r for r in fc_results if r['p'] < 0.05]
cf_sig = [r for r in cf_results if r['p'] < 0.05]

if fc_sig and not cf_sig:
    print(f"  ✓ UNIDIRECTIONAL: Friction → Compliance")
    print(f"    Past friction predicts future compliance at lags: "
          f"{', '.join(str(r['lag']) for r in fc_sig)} weeks")
    print(f"    Past compliance does NOT predict future friction.")
    print(f"    This supports the sequential mechanism hypothesis.")
elif cf_sig and not fc_sig:
    print(f"  ✓ UNIDIRECTIONAL: Compliance → Friction (REVERSE)")
    print(f"    Past compliance predicts future friction at lags: "
          f"{', '.join(str(r['lag']) for r in cf_sig)} weeks")
    print(f"    This is the OPPOSITE of the friction→compliance hypothesis.")
    print(f"    Possible explanation: compliance events trigger media/friction response.")
elif fc_sig and cf_sig:
    print(f"  ⚠ BIDIRECTIONAL: Both directions show Granger causality")
    print(f"    Friction → Compliance at lags: "
          f"{', '.join(str(r['lag']) for r in fc_sig)} weeks")
    print(f"    Compliance → Friction at lags: "
          f"{', '.join(str(r['lag']) for r in cf_sig)} weeks")
    print(f"    This suggests both types of events respond to a COMMON DRIVER")
    print(f"    rather than one causing the other.")
else:
    print(f"  ✗ NO GRANGER CAUSALITY in either direction")
    print(f"    Neither past friction nor past compliance helps predict the other.")
    print(f"    The co-occurrence is better explained by simultaneous response")
    print(f"    to shared triggers than by a lagged causal mechanism.")

# ── Also test on the original 30-row master CSV ─────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  ORIGINAL 30-ROW MASTER CSV (Index Scores)")
print(f"{'═' * 70}")

data_path = os.path.join(REPO_ROOT, 'Control_Proof',
                         'master_reflexive_correlation_data.csv')
df = pd.read_csv(data_path)
friction = df['Epstein_Friction_Index'].values.astype(float)
compliance = df['Institutional_Compliance_Index'].values.astype(float)

data_orig = pd.DataFrame({'compliance': compliance, 'friction': friction})
max_lag_orig = 4  # fewer lags due to small sample

print(f"\n  Rows: {len(df)}")
print(f"  Testing lags 1-{max_lag_orig} (limited by sample size)")

print(f"\n  ── Direction: Friction → Compliance ──")
print(f"  {'Lag':>6} {'F-stat':>10} {'p-value':>10} {'Sig?':>8}")
print(f"  {'─' * 34}")
try:
    gc_orig_fc = grangercausalitytests(data_orig[['compliance', 'friction']],
                                        maxlag=max_lag_orig, verbose=False)
    for lag in range(1, max_lag_orig + 1):
        f_stat = gc_orig_fc[lag][0]['ssr_ftest'][0]
        p_val = gc_orig_fc[lag][0]['ssr_ftest'][1]
        sig = "✓" if p_val < 0.05 else "✗"
        print(f"  {lag:>6} {f_stat:>10.4f} {p_val:>10.4f} {sig:>8}")
except Exception as exc:
    print(f"  Error: {exc}")

print(f"\n  ── Direction: Compliance → Friction ──")
print(f"  {'Lag':>6} {'F-stat':>10} {'p-value':>10} {'Sig?':>8}")
print(f"  {'─' * 34}")
try:
    gc_orig_cf = grangercausalitytests(data_orig[['friction', 'compliance']],
                                        maxlag=max_lag_orig, verbose=False)
    for lag in range(1, max_lag_orig + 1):
        f_stat = gc_orig_cf[lag][0]['ssr_ftest'][0]
        p_val = gc_orig_cf[lag][0]['ssr_ftest'][1]
        sig = "✓" if p_val < 0.05 else "✗"
        print(f"  {lag:>6} {f_stat:>10.4f} {p_val:>10.4f} {sig:>8}")
except Exception as exc:
    print(f"  Error: {exc}")

# ── Bottom line ──────────────────────────────────────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  BOTTOM LINE")
print(f"{'═' * 70}")
print(f"""
  Original pre-2026 datasets (Control_Proof, Project_Trident,
  Silicon_Sovereignty) — {n} weekly bins.

  Granger causality is a stronger test than simple correlation because it
  asks about PREDICTIVE direction, not just co-occurrence.

  "X Granger-causes Y" means: knowing past values of X improves our
  ability to predict current Y, beyond what past Y values alone provide.

  IMPORTANT CAVEATS:
    1. "Granger causality" is a statistical concept, NOT proof of real
       causation.  It tests predictive information flow, not mechanism.
    2. Both series having autocorrelation can inflate Granger results
       at low lags.
    3. Small sample sizes (30 rows for the original CSV) limit the
       statistical power and reliability of Granger tests.
    4. Granger tests assume stationarity — if the series have trends
       or structural breaks, results may be unreliable.

  WHAT THE RESULTS MEAN:
    • Unidirectional (Friction → Compliance): Supports the sequential
      mechanism hypothesis — friction events contain predictive information
      about future compliance events.
    • Unidirectional (Compliance → Friction): Suggests the REVERSE —
      compliance events predict friction (e.g., policy deals trigger
      media backlash).
    • Bidirectional: Both predict each other — likely driven by a common
      underlying driver (e.g., the political calendar).
    • No causality: The co-occurrence is simultaneous, not sequential —
      consistent with simultaneous response to shared triggers.
""")
print("=" * 70)
