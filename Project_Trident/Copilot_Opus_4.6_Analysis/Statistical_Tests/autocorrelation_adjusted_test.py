#!/usr/bin/env python3
"""
Autocorrelation-Adjusted Significance Test
Purpose: Standard permutation tests assume independent observations.  Weekly
         event counts are likely autocorrelated (a crisis lasts more than one
         week), which can inflate cross-correlation significance.  This script
         diagnoses autocorrelation via the Durbin-Watson statistic and then
         runs a block bootstrap that preserves temporal structure.

Planned item: "Autocorrelation-adjusted significance test (Durbin-Watson /
               block bootstrap)"

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

SEED = 42
rng = np.random.default_rng(SEED)


# ── Load datasets ────────────────────────────────────────────────────────────
print("=" * 70)
print("AUTOCORRELATION-ADJUSTED SIGNIFICANCE TEST")
print("=" * 70)
print("\nDurbin-Watson statistic + block bootstrap for weekly event counts")
print("Datasets: original pre-2026 (Control_Proof, Project_Trident, Silicon_Sovereignty)\n")

friction_events = load_friction_events()
compliance_events = load_compliance_events()
weekly = build_weekly_counts(friction_events, compliance_events)
f_series = weekly['friction'].values.astype(float)
c_series = weekly['compliance'].values.astype(float)
n = len(f_series)

r_obs, p_par = pearsonr(f_series, c_series)
rho_obs, _ = spearmanr(f_series, c_series)
print(f"\n  Weeks            : {n}")
print(f"  Observed Pearson : r = {r_obs:.4f}  (parametric p = {p_par:.6f})")
print(f"  Observed Spearman: ρ = {rho_obs:.4f}")

# ── 1. Durbin-Watson statistic ───────────────────────────────────────────
# DW tests autocorrelation in the residuals of a regression.
# DW ≈ 2 means no autocorrelation; DW < 1.5 suggests positive
# autocorrelation; DW > 2.5 suggests negative autocorrelation.
from statsmodels.stats.stattools import durbin_watson
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant

X = add_constant(f_series)
model = OLS(c_series, X).fit()
dw = durbin_watson(model.resid)

print(f"\n  ── Durbin-Watson Statistic ──")
print(f"  DW = {dw:.4f}")
if dw < 1.5:
    print(f"  Interpretation: POSITIVE autocorrelation detected (DW < 1.5)")
    print(f"  → Standard p-values are likely OVERSTATED (too optimistic)")
elif dw > 2.5:
    print(f"  Interpretation: NEGATIVE autocorrelation detected (DW > 2.5)")
else:
    print(f"  Interpretation: No strong autocorrelation (1.5 ≤ DW ≤ 2.5)")

# ── 2. Lag-1 autocorrelation for each series ─────────────────────────────
f_ac1 = np.corrcoef(f_series[:-1], f_series[1:])[0, 1]
c_ac1 = np.corrcoef(c_series[:-1], c_series[1:])[0, 1]
print(f"\n  ── Lag-1 Autocorrelation ──")
print(f"  Friction  lag-1 r = {f_ac1:.4f}")
print(f"  Compliance lag-1 r = {c_ac1:.4f}")

if max(f_ac1, c_ac1) > 0.3:
    print(f"  → Substantial autocorrelation detected; block bootstrap needed")
else:
    print(f"  → Mild autocorrelation; standard test may be acceptable")

# ── 3. Block bootstrap ───────────────────────────────────────────────────
# Instead of shuffling individual weeks (which destroys temporal structure),
# we shuffle blocks of consecutive weeks.  Block size is chosen based on
# the lag-1 autocorrelation: larger autocorrelation → larger blocks.
#
# Optimal block size (Politis & Romano, 1994): roughly 1 / (1 - ρ)
# but capped at n/4 and floored at 2.
# Optimal block size heuristic based on Politis & Romano (1994):
# block_size ≈ 1 / (1 - max_autocorrelation).
# Capped at n/4 to ensure enough blocks for meaningful resampling,
# and floored at 2 to maintain temporal structure.
# The 0.95 threshold prevents division-by-near-zero when autocorrelation
# is extreme, defaulting to n/4 (max 20) in that case.
max_ac = max(abs(f_ac1), abs(c_ac1))
if max_ac >= 0.95:
    block_size = min(n // 4, 20)
else:
    block_size = max(2, min(int(np.ceil(1.0 / (1.0 - max_ac))), n // 4))

N_BOOT = 10_000
print(f"\n  ── Block Bootstrap ({N_BOOT:,} iterations) ──")
print(f"  Block size: {block_size} weeks")
print(f"  (chosen based on max lag-1 autocorrelation = {max_ac:.4f})")

n_blocks = int(np.ceil(n / block_size))
boot_r = np.empty(N_BOOT)
boot_rho = np.empty(N_BOOT)

for i in range(N_BOOT):
    # Sample blocks with replacement, then truncate to length n
    starts = rng.integers(0, n - block_size + 1, size=n_blocks)
    indices = np.concatenate([np.arange(s, s + block_size) for s in starts])[:n]
    shuffled_f = f_series[indices]
    boot_r[i] = np.corrcoef(shuffled_f, c_series)[0, 1]
    boot_rho[i] = spearmanr(shuffled_f, c_series).statistic

# Empirical p-values from block bootstrap
p_r = (np.sum(np.abs(boot_r) >= np.abs(r_obs)) + 1) / (N_BOOT + 1)
p_rho = (np.sum(np.abs(boot_rho) >= np.abs(rho_obs)) + 1) / (N_BOOT + 1)

print(f"\n  Results (block bootstrap):")
print(f"    Pearson r  = {r_obs:.4f}  | block-bootstrap p = {p_r:.4f}")
print(f"    Spearman ρ = {rho_obs:.4f}  | block-bootstrap p = {p_rho:.4f}")

print(f"\n  Permuted distribution (Pearson):")
print(f"    Mean: {np.mean(boot_r):.4f}  Std: {np.std(boot_r):.4f}")
print(f"    5th percentile: {np.percentile(boot_r, 5):.4f}")
print(f"    95th percentile: {np.percentile(boot_r, 95):.4f}")

# ── 4. Comparison: standard vs adjusted significance ─────────────────────
print(f"\n  ── Comparison: Standard vs Adjusted Significance ──")
print(f"  {'Metric':<20} {'Standard p':>12} {'Block-boot p':>14} {'Change':>10}")
print(f"  {'─' * 56}")
print(f"  {'Pearson r':<20} {p_par:>12.6f} {p_r:>14.4f} {'↑' if p_r > p_par else '↓'}")

if p_r > 0.05 and p_par < 0.05:
    print(f"\n  ⚠ CRITICAL: Pearson significance DISAPPEARS after autocorrelation")
    print(f"    adjustment.  The standard test was overstating the evidence.")
elif p_r < 0.05 and p_par < 0.05:
    print(f"\n  ✓ Pearson significance SURVIVES autocorrelation adjustment.")
    if p_r > p_par * 5:
        print(f"    However, p-value increased substantially ({p_par:.6f} → {p_r:.4f}).")
        print(f"    The correlation is real but weaker than the standard test suggests.")
    else:
        print(f"    The correlation is robust to temporal structure.")
else:
    print(f"\n  Neither test finds significance at p < 0.05.")

# ── Bottom line ──────────────────────────────────────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  BOTTOM LINE")
print(f"{'═' * 70}")
print(f"""
  Original pre-2026 datasets (Control_Proof, Project_Trident,
  Silicon_Sovereignty) — {n} weekly bins.

  The Durbin-Watson statistic and lag-1 autocorrelation both check whether
  consecutive weekly observations are dependent on each other.  When they
  are, a standard permutation test (which shuffles individual weeks) can
  overstate significance by 10–30% or more.

  The block bootstrap preserves temporal structure by shuffling BLOCKS of
  consecutive weeks instead of individual observations.  This gives a
  fairer baseline for judging whether the observed correlation could arise
  by chance in time-series data.

  Results:
    DW = {dw:.4f}  |  Friction lag-1 = {f_ac1:.4f}
    Standard p (Pearson) = {p_par:.6f}
    Block-boot p (Pearson) = {p_r:.4f}
    Block-boot p (Spearman) = {p_rho:.4f}

  If both standard and block-bootstrap p-values are significant, the
  correlation is robust.  If only the standard test is significant but the
  block-bootstrap is not, autocorrelation was inflating the result.
""")
print("=" * 70)
