#!/usr/bin/env python3
"""
Permutation Test for Friction-Compliance Correlation
Purpose: Stress-test observed correlations by shuffling friction values and
         checking whether real correlations beat random noise.

Part 1 – 30-row master CSV  (original index-based dataset)
Part 2 – Multi-dataset test (event counts from BlackRock, Infrastructure,
         Timeline_Update, Anchors, Biopharma aggregated into weekly bins —
         ~213 weeks, ~1,000+ classified events)
"""

import os
import warnings
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

warnings.filterwarnings('ignore', category=FutureWarning)

SEED = 42
rng = np.random.default_rng(SEED)
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.join(script_dir, '..', '..', '..')


# ─────────────────────────────────────────────────────────────────────────────
#  Helper: summarise a permutation distribution
# ─────────────────────────────────────────────────────────────────────────────
def summarise(label, observed, perm_dist):
    """Print distribution summary and empirical p-value."""
    exceed = np.sum(np.abs(perm_dist) >= np.abs(observed))
    p_emp = (exceed + 1) / (len(perm_dist) + 1)   # conservative estimate

    print(f"\n{'=' * 70}")
    print(f"  {label}")
    print(f"{'=' * 70}")
    print(f"  Observed r           : {observed:.4f}")
    print(f"  Permuted distribution:")
    print(f"    Mean               : {np.mean(perm_dist):.4f}")
    print(f"    Std                : {np.std(perm_dist):.4f}")
    print(f"    Min                : {np.min(perm_dist):.4f}")
    print(f"    Max                : {np.max(perm_dist):.4f}")
    print(f"    5th percentile     : {np.percentile(perm_dist, 5):.4f}")
    print(f"    95th percentile    : {np.percentile(perm_dist, 95):.4f}")
    print(f"  |permuted| >= |observed| : {exceed} / {len(perm_dist)}")
    print(f"  Empirical p-value    : {p_emp:.4f}")

    if p_emp < 0.01:
        verdict = ("SIGNIFICANT (p < 0.01). The observed correlation is very "
                    "unlikely to arise by chance.")
    elif p_emp < 0.05:
        verdict = ("SIGNIFICANT (p < 0.05). The observed correlation is "
                    "unlikely to arise by chance.")
    elif p_emp < 0.10:
        verdict = ("MARGINAL (p < 0.10). Some evidence the correlation is "
                    "real, but not conclusive.")
    else:
        verdict = ("NOT SIGNIFICANT. The observed correlation could plausibly "
                    "be random noise.")

    print(f"  Verdict              : {verdict}")
    return p_emp


# ═════════════════════════════════════════════════════════════════════════════
#  PART 1 — 30-row master CSV (index-based, 1,000 permutations)
# ═════════════════════════════════════════════════════════════════════════════
N_PERM_PART1 = 1_000

data_path = os.path.join(repo_root, 'Control_Proof',
                         'master_reflexive_correlation_data.csv')
df = pd.read_csv(data_path)

friction = df['Epstein_Friction_Index'].values
compliance = df['Institutional_Compliance_Index'].values

print("=" * 70)
print("PART 1 — 30-row master CSV (index scores)")
print("=" * 70)
print(f"\nDataset : master_reflexive_correlation_data.csv")
print(f"Rows    : {len(df)}")
print(f"Shuffles: {N_PERM_PART1:,}")
print(f"Seed    : {SEED}")

r_direct, p_direct = pearsonr(friction, compliance)
lagged_friction = pd.Series(friction).shift(2).values
valid = ~np.isnan(lagged_friction)
r_lagged, p_lagged = pearsonr(lagged_friction[valid], compliance[valid])

print(f"\n--- Observed correlations ---")
print(f"  Direct (0-lag) : r = {r_direct:.4f}  (parametric p = {p_direct:.4f})")
print(f"  2-week lag     : r = {r_lagged:.4f}  (parametric p = {p_lagged:.4f})")

perm_direct = np.empty(N_PERM_PART1)
perm_lagged = np.empty(N_PERM_PART1)
for i in range(N_PERM_PART1):
    shuffled = rng.permutation(friction)
    perm_direct[i] = np.corrcoef(shuffled, compliance)[0, 1]
    shifted = np.empty_like(shuffled, dtype=float)
    shifted[:2] = np.nan
    shifted[2:] = shuffled[:-2]
    mask = ~np.isnan(shifted)
    perm_lagged[i] = np.corrcoef(shifted[mask], compliance[mask])[0, 1]

summarise("PART 1 · DIRECT (0-lag)", r_direct, perm_direct)
summarise("PART 1 · 2-WEEK LAG", r_lagged, perm_lagged)


# ═════════════════════════════════════════════════════════════════════════════
#  PART 2 — Multi-dataset permutation test (event counts → weekly bins)
# ═════════════════════════════════════════════════════════════════════════════
N_PERM_PART2 = 10_000          # more permutations → finer p-value resolution

print("\n\n" + "#" * 70)
print("#  PART 2 — Multi-dataset event-count test (10,000 permutations)")
print("#" * 70)

# ── Event classification rules ───────────────────────────────────────────────
friction_categories = {
    'Crisis_Event', 'Political_Event', 'Media_Reaction', 'Conflict',
    'Legislation', 'Ritual_Event', 'Political_Org', 'Holiday',
}
compliance_categories = {
    'Strategic_Shift', 'Government_Ties', 'Crypto_Pivot', 'Crypto_Sentiment',
    'ESG_Policy', 'ESG_Origins', 'Tech_Dominance', 'Policy', 'Geopolitics',
    'Corporate', 'FDA_Reg', 'Funding', 'Federal_Contract',
    'Corporate_Action', 'Financial_Performance', 'Clinical_Milestone',
    'General_Update',
}

# ── Load & classify events ───────────────────────────────────────────────────
dataset_files = {
    'blackrock':       'New_Data_2026/BlackRock_Timeline_Full_Decade.csv',
    'infrastructure':  'New_Data_2026/Infrastructure_Forensics.csv',
    'timeline_update': 'New_Data_2026/Timeline_Update_Jan2026_Corrected (1).csv',
    'anchors':         'New_Data_2026/Additional_Anchors_Jan2026_Final.csv',
    'biopharma':       'New_Data_2026/Biopharma.csv',
}
dataset_files_full = {
    **dataset_files,
    'high_growth': 'New_Data_2026/High_Growth_Companies_2015_2026.csv',
}


def classify_events(file_map):
    """Load CSVs, classify each row as friction / compliance, return DataFrame."""
    rows = []
    for name, relpath in file_map.items():
        path = os.path.join(repo_root, relpath)
        try:
            raw = pd.read_csv(path)
        except FileNotFoundError:
            print(f"  ⚠ skipping {relpath} (file not found)")
            continue
        except Exception as exc:
            print(f"  ⚠ skipping {relpath} ({exc})")
            continue

        # detect date and category columns
        date_col = next((c for c in ['date', 'Date', 'event_date',
                                      'publication_date', 'action_date']
                         if c in raw.columns), None)
        cat_col = next((c for c in ['category', 'Category', 'event_type',
                                     'type']
                        if c in raw.columns), None)
        if not date_col or not cat_col:
            continue

        for _, row in raw.iterrows():
            try:
                d = pd.to_datetime(row[date_col])
                cat = row[cat_col]
            except (ValueError, TypeError, KeyError):
                continue
            if cat in friction_categories:
                rows.append({'date': d, 'type': 'friction', 'source': name})
            elif cat in compliance_categories:
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


def run_multi_permutation(label, file_map):
    """Classify events, aggregate by week, run permutation test."""
    print(f"\n{'─' * 70}")
    print(f"  {label}")
    print(f"{'─' * 70}")

    events = classify_events(file_map)
    n_friction = (events['type'] == 'friction').sum()
    n_compliance = (events['type'] == 'compliance').sum()
    print(f"  Events classified : {len(events)}  "
          f"(friction {n_friction}, compliance {n_compliance})")

    weekly = build_weekly(events)
    f_series = weekly['friction'].values.astype(float)
    c_series = weekly['compliance'].values.astype(float)
    n_weeks = len(f_series)
    print(f"  Weekly bins       : {n_weeks}")

    # observed Pearson & Spearman
    r_obs, p_par = pearsonr(f_series, c_series)
    rho_obs, _ = spearmanr(f_series, c_series)
    print(f"  Observed Pearson  : r = {r_obs:.4f}  (parametric p = {p_par:.6f})")
    print(f"  Observed Spearman : ρ = {rho_obs:.4f}")

    # permutation loop — shuffle weekly friction counts
    perm_r = np.empty(N_PERM_PART2)
    perm_rho = np.empty(N_PERM_PART2)
    for i in range(N_PERM_PART2):
        shuf = rng.permutation(f_series)
        perm_r[i] = np.corrcoef(shuf, c_series)[0, 1]
        perm_rho[i] = spearmanr(shuf, c_series).statistic

    summarise(f"{label} · Pearson r", r_obs, perm_r)
    summarise(f"{label} · Spearman ρ (rank-based, outlier-resistant)", rho_obs,
              perm_rho)


# ── Run both scopes ──────────────────────────────────────────────────────────
print("\nLoading and classifying events from New_Data_2026/ ...")
run_multi_permutation("CORE scope (excl. High_Growth_Companies)", dataset_files)
run_multi_permutation("FULL scope (incl. High_Growth_Companies)",
                      dataset_files_full)


# ═════════════════════════════════════════════════════════════════════════════
#  BOTTOM LINE + DATA-QUALITY RECOMMENDATIONS
# ═════════════════════════════════════════════════════════════════════════════
print("\n\n" + "=" * 70)
print("  BOTTOM LINE")
print("=" * 70)
print("""
  Part 1 tested the original 30-row index-score dataset.
  Part 2 tested the full multi-dataset event counts (~1,000+ events,
  ~213 weekly bins) in two scopes:
    • Core  – strategic institutional events only
    • Full  – adds biotech operational events (High_Growth_Companies)

  The permutation test shuffles friction values thousands of times and
  checks how often random noise produces a correlation as strong as
  (or stronger than) the real one.  If the empirical p-value is small
  (< 0.05), the pattern is unlikely to be a coincidence.
""")

print("=" * 70)
print("  RECOMMENDATIONS FOR MORE ACCURATE RESULTS")
print("=" * 70)
print("""
  1. STANDARDISE DATE FORMATS
     Some CSVs use different date columns ('date', 'Date',
     'event_date', etc.) and inconsistent formats.  Pick one
     column name and one format (ISO 8601: YYYY-MM-DD) across
     every file.  Rows that fail to parse are silently dropped
     right now — that costs you data.

  2. STANDARDISE CATEGORY LABELS
     Friction / compliance classification depends on matching
     exact category strings.  Typos or new labels (e.g. 'Other')
     fall through the cracks.  Keep a single lookup table of
     allowed categories and validate every CSV against it before
     analysis.

  3. FILL GAPS IN THE TIMELINE
     Weeks with zero events in BOTH columns still matter — they
     tell the model "nothing happened here."  The current code
     fills gaps with 0, which is correct, but make sure every
     dataset actually covers the full 2020-2026 window.  Datasets
     that only cover Dec 2025 (like Timeline_Update) will create
     a spike that inflates the correlation.

  4. ADD A SPEARMAN / RANK TEST
     Pearson r is sensitive to outliers and assumes a linear
     relationship.  Spearman ρ (included above) ranks the data
     first, so one monster week can't drag the whole number.  If
     Pearson and Spearman agree, the signal is robust.

  5. INCREASE PERMUTATIONS
     1,000 shuffles can only resolve p-values down to ~0.001.
     Part 2 already uses 10,000; you could go to 100,000 if you
     want finer resolution (takes a few minutes).

  6. WATCH OUT FOR AUTOCORRELATION
     Weekly event counts are often correlated with their own
     recent past (e.g. a crisis drags on for weeks).  A basic
     permutation test ignores this and can overstate significance.
     A block-shuffle or phase-randomisation test (more advanced)
     preserves that time structure and gives a fairer baseline.

  7. CONSIDER SPEARMAN OVER PEARSON AS PRIMARY METRIC
     With messy, scraped data that may have outlier weeks,
     Spearman ρ is generally more trustworthy than Pearson r.
     Report both, but lean on Spearman for your headline number.

  8. SEPARATE "WHAT HAPPENED" FROM "HOW MUCH"
     Right now friction and compliance are raw event counts.
     A week with 1 major leak and a week with 1 minor press
     mention both count as "1."  If you can add a severity or
     impact score (even 1-3 scale), a weighted correlation will
     be more meaningful.
""")
print("=" * 70)
