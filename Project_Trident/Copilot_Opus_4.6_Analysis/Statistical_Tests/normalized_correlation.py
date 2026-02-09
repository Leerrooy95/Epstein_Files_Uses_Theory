#!/usr/bin/env python3
"""
Normalized Event-Count Correlation
Purpose: The raw weekly event-count correlation is dominated by periods with
         far more events than others.  This script normalizes event counts so
         that each year contributes equally, then re-computes the
         friction-compliance correlation.

Planned item: "Normalized event-count correlation (events per year equalized)"

If the correlation survives normalization, it reflects genuine week-to-week
co-movement rather than a magnitude artifact from any single period.

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

print("=" * 70)
print("NORMALIZED EVENT-COUNT CORRELATION")
print("=" * 70)
print("\nEqualizes each year's contribution before computing correlations.")
print("Datasets: original pre-2026 (Control_Proof, Project_Trident, Silicon_Sovereignty)\n")

friction_events = load_friction_events()
compliance_events = load_compliance_events()
weekly = build_weekly_counts(friction_events, compliance_events)
f_raw = weekly['friction'].values.astype(float)
c_raw = weekly['compliance'].values.astype(float)
n = len(f_raw)

# Raw correlation (baseline)
r_raw, p_raw = pearsonr(f_raw, c_raw)
rho_raw, _ = spearmanr(f_raw, c_raw)
print(f"\n  ── Raw (un-normalized) ──")
print(f"  Weeks: {n}  |  Pearson r = {r_raw:.4f} (p={p_raw:.6f})  |  Spearman ρ = {rho_raw:.4f}")

# ── Method 1: Per-year z-score normalization ─────────────────────────────
# Within each year, subtract the year's mean and divide by the year's std.
# This removes the "one year has more events" effect while preserving the
# within-year weekly pattern.
weekly_copy = weekly.copy()
week_starts = weekly_copy.index.to_timestamp()
weekly_copy['year'] = week_starts.year

f_norm = np.zeros(n)
c_norm = np.zeros(n)
for yr in weekly_copy['year'].unique():
    mask = weekly_copy['year'] == yr
    idx = np.where(mask)[0]
    fv = f_raw[idx]
    cv = c_raw[idx]
    # z-score (handle constant series by defaulting std to 1.0)
    f_std = fv.std()
    c_std = cv.std()
    f_std = f_std if f_std > 0 else 1.0
    c_std = c_std if c_std > 0 else 1.0
    f_norm[idx] = (fv - fv.mean()) / f_std
    c_norm[idx] = (cv - cv.mean()) / c_std

r_zscore, p_zscore = pearsonr(f_norm, c_norm)
rho_zscore, _ = spearmanr(f_norm, c_norm)
print(f"\n  ── Method 1: Per-Year Z-Score ──")
print(f"  Pearson r = {r_zscore:.4f} (p={p_zscore:.6f})  |  Spearman ρ = {rho_zscore:.4f}")
print(f"  Change from raw: Pearson {r_raw:.4f} → {r_zscore:.4f} "
      f"({'↓' if r_zscore < r_raw else '↑'} {abs(r_raw - r_zscore):.4f})")

# ── Method 2: Per-year proportional scaling ──────────────────────────────
# Scale each year's weekly counts so that total events per year are equal.
# This preserves within-year relative patterns but removes inter-year
# magnitude differences.
target_total = 100  # arbitrary constant per year
f_scaled = np.zeros(n)
c_scaled = np.zeros(n)
for yr in weekly_copy['year'].unique():
    mask = weekly_copy['year'] == yr
    idx = np.where(mask)[0]
    fv = f_raw[idx]
    cv = c_raw[idx]
    f_total = fv.sum() if fv.sum() > 0 else 1
    c_total = cv.sum() if cv.sum() > 0 else 1
    f_scaled[idx] = fv * (target_total / f_total)
    c_scaled[idx] = cv * (target_total / c_total)

r_scaled, p_scaled = pearsonr(f_scaled, c_scaled)
rho_scaled, _ = spearmanr(f_scaled, c_scaled)
print(f"\n  ── Method 2: Per-Year Proportional Scaling ──")
print(f"  Pearson r = {r_scaled:.4f} (p={p_scaled:.6f})  |  Spearman ρ = {rho_scaled:.4f}")
print(f"  Change from raw: Pearson {r_raw:.4f} → {r_scaled:.4f} "
      f"({'↓' if r_scaled < r_raw else '↑'} {abs(r_raw - r_scaled):.4f})")

# ── Method 3: Binary (presence/absence) ──────────────────────────────────
# Convert all non-zero weeks to 1.  This completely removes magnitude
# and asks: "do friction and compliance tend to occur in the same weeks?"
f_binary = (f_raw > 0).astype(float)
c_binary = (c_raw > 0).astype(float)
r_binary, p_binary = pearsonr(f_binary, c_binary)
rho_binary, _ = spearmanr(f_binary, c_binary)
print(f"\n  ── Method 3: Binary (presence/absence) ──")
print(f"  Pearson r = {r_binary:.4f} (p={p_binary:.6f})  |  Spearman ρ = {rho_binary:.4f}")
print(f"  Weeks with friction: {int(f_binary.sum())}/{n}")
print(f"  Weeks with compliance: {int(c_binary.sum())}/{n}")
print(f"  Weeks with both: {int((f_binary * c_binary).sum())}/{n}")

# ── Summary comparison ───────────────────────────────────────────────────
print(f"\n  ── Summary ──")
print(f"  {'Method':<30} {'Pearson r':>10} {'p-value':>12} {'Spearman ρ':>12}")
print(f"  {'─' * 64}")
print(f"  {'Raw (un-normalized)':<30} {r_raw:>10.4f} {p_raw:>12.6f} {rho_raw:>12.4f}")
print(f"  {'Per-year z-score':<30} {r_zscore:>10.4f} {p_zscore:>12.6f} {rho_zscore:>12.4f}")
print(f"  {'Per-year proportional':<30} {r_scaled:>10.4f} {p_scaled:>12.6f} {rho_scaled:>12.4f}")
print(f"  {'Binary (presence/absence)':<30} {r_binary:>10.4f} {p_binary:>12.6f} {rho_binary:>12.4f}")

if r_zscore > 0.3 and p_zscore < 0.05:
    print(f"\n  ✓ Correlation SURVIVES z-score normalization (r={r_zscore:.4f})")
    print(f"    The co-movement is not just a magnitude artifact.")
elif r_zscore > 0.1 and p_zscore < 0.05:
    print(f"\n  ⚠ Weak correlation survives normalization (r={r_zscore:.4f})")
    print(f"    Some real signal, but much weaker than the raw number suggests.")
else:
    print(f"\n  ✗ Correlation DOES NOT survive normalization (r={r_zscore:.4f})")
    print(f"    The raw r ≈ {r_raw:.2f} was driven by magnitude differences across years.")

# ── Bottom line ──────────────────────────────────────────────────────────
print(f"\n\n{'═' * 70}")
print(f"  BOTTOM LINE")
print(f"{'═' * 70}")
print(f"""
  Original pre-2026 datasets (Control_Proof, Project_Trident,
  Silicon_Sovereignty) — {n} weekly bins.

  Three normalization approaches test whether the pattern is real:

  1. Z-SCORE: Removes each year's mean and scales by its std.
     If the within-year weekly pattern is genuinely correlated,
     this preserves it while removing the inter-year magnitude gap.

  2. PROPORTIONAL SCALING: Makes every year's total event count equal.
     Preserves the relative weekly distribution within each year.

  3. BINARY: Ignores magnitude entirely.  Asks only "do friction and
     compliance tend to occur in the same weeks or different weeks?"

  If ALL THREE methods show significant correlation, the signal is real.
  If ONLY the raw method shows significance, the result is a magnitude
  artifact driven by event concentration in certain periods.
""")
print("=" * 70)
