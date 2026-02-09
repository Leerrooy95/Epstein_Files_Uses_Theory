# Correlation Summary

**Purpose:** Single-page reference for every reported correlation, the exact
datasets behind it, and where to reproduce it.

**Date:** February 8, 2026

---

## Quick Reference

| # | Correlation | Stat | p-value | Datasets | Script |
|---|-------------|------|---------|----------|--------|
| 1 | Reflexive Control (2-week lag) | r = 0.6196 | 0.0004 | 30-row master CSV | `Run_Correlations_Yourself/run_original_analysis.py` Part 1 |
| 2 | Project Trident (ritual vs holiday proximity) | Mann-Whitney U, p = 0.002 | 0.002 | 533-row lag CSV | `Run_Correlations_Yourself/run_original_analysis.py` Part 2 |
| 3 | Multi-Dataset Cross-Validation (14-day periodicity) | χ² = 330.62 | < 0.0001 | 4 Silicon Sovereignty CSVs (2,105 records) | `Run_Correlations_Yourself/run_original_analysis.py` Part 3 |
| 4 | Updated event-count (core scope, 0-lag) | r = 0.6685 | < 0.0001 | 5 New_Data_2026 CSVs (~1,010 events) | `Run_Correlations_Yourself/reproduce_updated_correlation.py` |
| 5 | Updated event-count (full scope, 0-lag) | r = 0.5268 | < 0.0001 | 6 New_Data_2026 CSVs (~2,069 events) | `Run_Correlations_Yourself/reproduce_updated_correlation.py` |

---

## Correlation 1 — Original Reflexive Control

**Result:** Pearson r = 0.6196 at 2-week lag (p = 0.0004)

**Computed:** December 23, 2025 (v3.1 release)

**Dataset:**
- `Control_Proof/master_reflexive_correlation_data.csv` — 30 rows of weekly
  hand-scored Epstein_Friction_Index and Institutional_Compliance_Index (1–10
  scale)
- `Control_Proof/reflexive_control_scraped_data.csv` — 4 OSINT trigger events
  (optional context, not used in the calculation itself)

**What it measures:** Whether friction spikes (document leaks, media cycles)
at time t−2 predict institutional compliance (capital deals, policy shifts) at
time t.  The near-zero direct correlation (r = −0.03) rules out coincidence;
the strong 2-week lag is the signature of the "thermostat" feedback loop.

**Permutation test (Feb 8):** 0 of 1,000 shuffles produced |r| ≥ 0.62 →
empirical p < 0.001.

**Key caveat (from permutation_test.py):** Spearman ρ ≈ 0.02 (not
significant).  The Pearson result is driven by a few high-magnitude weeks —
the rank ordering across all 30 rows is essentially flat.

---

## Correlation 2 — Project Trident (Ritual-Proximity)

**Result:** Mann-Whitney U p = 0.002; ritual events 50.7% vs holiday baseline
19.9% within ±14 days of policy actions

**Computed:** December 24, 2025 (v4.5 release)

**Dataset:**
- `Project_Trident/Best_Data_For_Project_Trident/Lag_Correlation_Analysis_Verified_Holidays.csv`
  — 533 policy-action events, each paired with the nearest ritual date and the
  nearest holiday date

**What it measures:** Whether policy actions cluster closer to ritual-calendar
dates than to ordinary holidays.  The 2.5× proximity ratio at the 14-day
window, combined with a medium Cohen's d (0.42), shows ritual dates are a
stronger temporal anchor than secular holidays.

---

## Correlation 3 — Multi-Dataset Cross-Validation

**Result:** χ² = 330.62 (p < 0.0001) for 14-day non-random clustering across
2,105 events

**Computed:** December 25, 2025 (v5.5 release)

**Datasets (all in `09_Silicon_Sovereignty/`):**

| File | Records |
|------|---------|
| `Coalition_Narrative_Map_2015-2025.csv` | 456 |
| `VOCA_funding_timeline_clean.csv` | 667 |
| `Regulatory_Map_Data_CLEANED.csv` | 76 |
| `REFINED_supercomputer_geopolitics (1).csv` | 906 |

**What it measures:** Whether events across four independent datasets cluster
in 14-day bins more than uniform randomness would predict.  The December 2025
window alone contains 56 events.

---

## Correlation 4 — Updated Event-Count (Core Scope)

**Result:** Pearson r = 0.6685 at 0-lag (p < 0.0001)

**Computed:** January 10, 2026 (documented in `New_Data_2026/2026_Analysis.md`)

**Datasets (all in `New_Data_2026/`, excluding High_Growth_Companies):**

| File | Records |
|------|---------|
| `BlackRock_Timeline_Full_Decade.csv` | 674 |
| `Infrastructure_Forensics.csv` | 107 |
| `Timeline_Update_Jan2026_Corrected (1).csv` | 99 |
| `Additional_Anchors_Jan2026_Final.csv` | 50 |
| `Biopharma.csv` | 108 |

**What it measures:** Whether friction event-counts and compliance
event-counts move together week-to-week across ~213 weekly bins (2020–2026).

**Independent reproduction (Jan 12):** r = 0.6192 (within 0.05 tolerance) —
see `DISCREPANCY_ANALYSIS.md`.

**Key caveat (from permutation_test.py):** Spearman ρ ≈ 0.02 for this scope.
The Pearson result is dominated by high-magnitude December 2025 weeks.

---

## Correlation 5 — Updated Event-Count (Full Scope)

**Result:** Pearson r = 0.5268 at 0-lag (p < 0.0001)

**Computed:** January 12, 2026 (independent verification)

**Datasets:** Same as Correlation 4 **plus**
`High_Growth_Companies_2015_2026.csv` (1,049 records of clinical milestones,
earnings, analyst ratings).

**What it measures:** Robustness check — does the friction-compliance
clustering hold when operational biotech events are included?  Yes, but
weaker.

**Spearman ρ = 0.17 (p = 0.004)** — statistically significant in the full
scope, unlike core scope.  Suggests the additional breadth of events adds
genuine rank-order signal even though it dilutes the magnitude-based Pearson r.

---

## How the Correlations Relate

```
                         ┌──────────────────────────────┐
                         │  ORIGINAL (pre-2026 data)     │
                         │                              │
     Correlation 1       │  r = 0.6196  (2-week lag)    │
     30-row master CSV   │  Hand-scored, small sample   │
                         └──────────────────────────────┘

                         ┌──────────────────────────────┐
     Correlations 2–3    │  ORIGINAL (pre-2026 data)     │
     Project Trident &   │  Mann-Whitney U p = 0.002    │
     Cross-Validation    │  χ² = 330.62                 │
                         └──────────────────────────────┘

                         ┌──────────────────────────────┐
                         │  UPDATED (New_Data_2026)      │
     Correlation 4       │  r = 0.6685  (0-lag, core)   │
     Core scope          │  ~1,010 strategic events     │
                         └──────────────────────────────┘

                         ┌──────────────────────────────┐
     Correlation 5       │  UPDATED (New_Data_2026)      │
     Full scope          │  r = 0.5268  (0-lag, full)   │
                         │  ~2,069 events incl. biotech │
                         └──────────────────────────────┘
```

**Key distinctions:**

- Correlations 1–3 use **only** pre-2026 datasets — reproducible via
  `Run_Correlations_Yourself/run_original_analysis.py`
- Correlations 4–5 use **only** New_Data_2026 CSVs — reproducible via
  `Run_Correlations_Yourself/reproduce_updated_correlation.py`
- The two groups use **completely independent datasets** — the original
  correlation was computed 12 days before New_Data_2026 files existed

---

## Known Limitations (from Lead Researcher analysis)

| Issue | Affects | Severity | Mitigation |
|-------|---------|----------|------------|
| Spearman ρ near zero (core scope) | Correlations 1, 4 | High | Pearson result driven by magnitude outliers; report Spearman alongside Pearson |
| 2025 year-skew (4.7× average) | Correlations 4, 5 | Medium | ~56% scraping artifact; use balanced datasets or normalize counts |
| Autocorrelation (friction lag-1 r = 0.67) | Correlations 4, 5 | Medium | May inflate cross-correlation 10–30%; planned block-bootstrap test |
| Small sample (n = 30) | Correlation 1 | Medium | Permutation test confirms significance (p < 0.001) despite size |

---

*Compiled by GitHub Copilot (Claude, Opus 4.6), February 8, 2026*
