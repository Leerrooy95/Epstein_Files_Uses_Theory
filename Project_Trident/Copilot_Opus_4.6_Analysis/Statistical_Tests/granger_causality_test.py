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

Datasets used: local copies in ../Datasets/ (originals in New_Data_2026/)
"""

import os
import warnings
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

warnings.filterwarnings('ignore', category=FutureWarning)

script_dir = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(script_dir, '..', 'Datasets')
repo_root = os.path.join(script_dir, '..', '..', '..')

# ── Event classification (same rules as other scripts) ───────────────────────
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
print("GRANGER CAUSALITY TEST")
print("=" * 70)
print("\nTests whether past friction predicts future compliance (or vice versa).")
print("Uses the statsmodels Granger causality implementation.\n")


def run_granger(label, file_map):
    """Run Granger causality tests for both directions."""
    print(f"\n{'═' * 70}")
    print(f"  {label}")
    print(f"{'═' * 70}")

    events = classify_events(file_map, datasets_dir)
    weekly = build_weekly(events)
    f_series = weekly['friction'].values.astype(float)
    c_series = weekly['compliance'].values.astype(float)
    n = len(f_series)

    r_obs, p_obs = pearsonr(f_series, c_series)
    print(f"\n  Weeks: {n}")
    print(f"  Observed Pearson r = {r_obs:.4f} (p={p_obs:.6f})")

    # ── Granger causality test ───────────────────────────────────────────────
    # statsmodels.tsa.stattools.grangercausalitytests tests whether the
    # lagged values of one series improve prediction of the other series
    # beyond the other series' own lagged values.
    #
    # It runs F-tests and chi-squared tests at each specified lag.
    from statsmodels.tsa.stattools import grangercausalitytests

    # Prepare data as a DataFrame with two columns
    data = pd.DataFrame({'compliance': c_series, 'friction': f_series})

    max_lag = 8  # test lags 1-8 weeks

    # ── Direction 1: Does friction Granger-cause compliance? ─────────────────
    print(f"\n  ── Direction 1: Friction → Compliance ──")
    print(f"  (Does past friction help predict current compliance?)")
    print(f"\n  {'Lag (weeks)':>12} {'F-statistic':>14} {'p-value':>10} {'Significant?':>14}")
    print(f"  {'─' * 50}")

    # grangercausalitytests expects [Y, X] — tests whether X Granger-causes Y
    # So for "friction → compliance", we pass [compliance, friction]
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

    return fc_results, cf_results


res_core = run_granger("CORE scope (excl. High_Growth_Companies)", CORE_FILES)
res_full = run_granger("FULL scope (incl. High_Growth_Companies)", FULL_FILES)

# ── Also test on the original 30-row master CSV ─────────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  ORIGINAL 30-ROW MASTER CSV (Index Scores)")
print(f"{'═' * 70}")

data_path = os.path.join(repo_root, 'Control_Proof',
                         'master_reflexive_correlation_data.csv')
df = pd.read_csv(data_path)
friction = df['Epstein_Friction_Index'].values.astype(float)
compliance = df['Institutional_Compliance_Index'].values.astype(float)

from statsmodels.tsa.stattools import grangercausalitytests

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


# ── Bottom line ──────────────────────────────────────────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  BOTTOM LINE")
print(f"{'═' * 70}")
print(f"""
  Granger causality is a stronger test than simple correlation because it
  asks about PREDICTIVE direction, not just co-occurrence.

  "X Granger-causes Y" means: knowing past values of X improves our
  ability to predict current Y, beyond what past Y values alone provide.

  IMPORTANT CAVEATS:
    1. "Granger causality" is a statistical concept, NOT proof of real
       causation.  It tests predictive information flow, not mechanism.
    2. Both series having autocorrelation (which they do — DW ≈ 1.29 for
       core scope) can inflate Granger results at low lags.
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
      consistent with the event-study framework's finding of colocation
      rather than causation.
""")
print("=" * 70)
