#!/usr/bin/env python3
"""
Permutation Test for Friction-Compliance Correlation
Purpose: Stress-test observed correlations by shuffling friction values and
         checking whether real correlations beat random noise.

Part 1 – 30-row master CSV  (original index-based dataset)
Part 2 – Multi-dataset test (event counts from original pre-2026 datasets
         — Control_Proof, Project_Trident, Silicon_Sovereignty — aggregated
         into weekly bins via original_data_loader)
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
#  PART 2 — Original pre-2026 datasets permutation test (event counts → weekly bins)
# ═════════════════════════════════════════════════════════════════════════════
N_PERM_PART2 = 10_000          # more permutations → finer p-value resolution

from original_data_loader import load_friction_events, load_compliance_events, build_weekly_counts

print("\n\n" + "#" * 70)
print("#  PART 2 — Original pre-2026 datasets event-count test (10,000 permutations)")
print("#" * 70)

# ── Load events from original datasets ───────────────────────────────────────
print("\nLoading friction events from original datasets ...")
friction_events = load_friction_events()
print(f"  Friction events loaded : {len(friction_events)}")

print("Loading compliance events from original datasets ...")
compliance_events = load_compliance_events()
print(f"  Compliance events loaded : {len(compliance_events)}")

# ── Build weekly counts ──────────────────────────────────────────────────────
weekly = build_weekly_counts(friction_events, compliance_events)
f_series = weekly['friction'].values.astype(float)
c_series = weekly['compliance'].values.astype(float)
n_weeks = len(f_series)

print(f"\n  Weekly bins       : {n_weeks}")
print(f"  Date range        : {weekly.index.min()} → {weekly.index.max()}")

# ── Observed correlations ────────────────────────────────────────────────────
r_obs, p_par = pearsonr(f_series, c_series)
rho_obs, _ = spearmanr(f_series, c_series)
print(f"  Observed Pearson  : r = {r_obs:.4f}  (parametric p = {p_par:.6f})")
print(f"  Observed Spearman : ρ = {rho_obs:.4f}")

# ── Permutation loop — shuffle weekly friction counts ────────────────────────
perm_r = np.empty(N_PERM_PART2)
perm_rho = np.empty(N_PERM_PART2)
for i in range(N_PERM_PART2):
    shuf = rng.permutation(f_series)
    perm_r[i] = np.corrcoef(shuf, c_series)[0, 1]
    perm_rho[i] = spearmanr(shuf, c_series).statistic

summarise("PART 2 · Pearson r (original pre-2026 datasets)", r_obs, perm_r)
summarise("PART 2 · Spearman ρ (rank-based, outlier-resistant)", rho_obs,
          perm_rho)


# ═════════════════════════════════════════════════════════════════════════════
#  BOTTOM LINE + DATA-QUALITY RECOMMENDATIONS
# ═════════════════════════════════════════════════════════════════════════════
print("\n\n" + "=" * 70)
print("  BOTTOM LINE")
print("=" * 70)
print("""
  Part 1 tested the original 30-row index-score dataset.
  Part 2 tested the original pre-2026 datasets (Control_Proof,
  Project_Trident, Silicon_Sovereignty) aggregated into weekly
  friction / compliance event counts.

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
     dataset actually covers the full date range.

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
