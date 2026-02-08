#!/usr/bin/env python3
"""
Permutation Test for Friction-Compliance Correlation
Purpose: Stress-test observed correlation by shuffling friction dates 1,000 times
         to determine if the correlation is statistically significant or random noise.
"""

import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# ── Configuration ────────────────────────────────────────────────────────────
N_PERMUTATIONS = 1_000
SEED = 42  # reproducible results

# ── Load data ────────────────────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'Control_Proof',
                         'master_reflexive_correlation_data.csv')
df = pd.read_csv(data_path)

friction = df['Epstein_Friction_Index'].values
compliance = df['Institutional_Compliance_Index'].values

print("=" * 70)
print("PERMUTATION TEST – Friction / Compliance Correlation")
print("=" * 70)
print(f"\nDataset : master_reflexive_correlation_data.csv")
print(f"Rows    : {len(df)}")
print(f"Shuffles: {N_PERMUTATIONS:,}")
print(f"Seed    : {SEED}")

# ── Observed correlations ────────────────────────────────────────────────────
r_direct, p_direct = pearsonr(friction, compliance)

lagged_friction = pd.Series(friction).shift(2).values
valid = ~np.isnan(lagged_friction)
r_lagged, p_lagged = pearsonr(lagged_friction[valid], compliance[valid])

print(f"\n--- Observed correlations ---")
print(f"  Direct (0-lag) : r = {r_direct:.4f}  (parametric p = {p_direct:.4f})")
print(f"  2-week lag     : r = {r_lagged:.4f}  (parametric p = {p_lagged:.4f})")

# ── Permutation loop ────────────────────────────────────────────────────────
rng = np.random.default_rng(SEED)

perm_direct = np.empty(N_PERMUTATIONS)
perm_lagged = np.empty(N_PERMUTATIONS)

for i in range(N_PERMUTATIONS):
    shuffled = rng.permutation(friction)

    # direct
    perm_direct[i] = np.corrcoef(shuffled, compliance)[0, 1]

    # 2-week lag
    shifted = np.empty_like(shuffled, dtype=float)
    shifted[:2] = np.nan
    shifted[2:] = shuffled[:-2]
    mask = ~np.isnan(shifted)
    perm_lagged[i] = np.corrcoef(shifted[mask], compliance[mask])[0, 1]

# ── Results ──────────────────────────────────────────────────────────────────
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

summarise("DIRECT (0-lag) correlation", r_direct, perm_direct)
summarise("2-WEEK LAG correlation", r_lagged, perm_lagged)

# ── Honest bottom-line ──────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  BOTTOM LINE")
print("=" * 70)
print("""
  This test shuffled the Friction Index values 1,000 times and
  recomputed the correlation each time.  If the real correlation
  sits well outside the cloud of random values, the pattern is
  unlikely to be a coincidence.  If it sits inside, you can't
  rule out chance.

  Check the empirical p-values above — they tell you the fraction
  of random shuffles that produced a correlation at least as
  extreme as the one you observed.
""")
print("=" * 70)
