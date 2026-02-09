# The Regulated Friction Project v8.3

A data-driven analysis of temporal correlations between friction events, policy shifts, and capital flows (2015-2026).

New to this project? See [Glossary.md](https://github.com/Leerrooy95/The_Regulated_Friction_Project/blob/main/Glossary.md)

---

## Table of Contents
- [Quick Summary](#quick-summary)
- [Understanding the Statistics](#understanding-the-statistics)
- [Key Statistics](#key-statistics)
- [The Convergence Model](#the-convergence-model)
- [The Three-Layer Model](#the-three-layer-model)
- [Repository Structure](#repository-structure)
- [What's New (v8.3)](#whats-new-v83---february-2026)
- [Quick Navigation by Type](#quick-navigation-by-type)
- [For Researchers](#for-researchers)
- [For Policymakers & Journalists](#for-policymakers--journalists)
- [Methodology](#methodology)
- [Limitations & Disclaimer](#limitations--disclaimer)
- [Connected Repositories](#connected-repositories)
- [Statistical Validation](#statistical-validation)

---

## Quick Summary

This repository documents statistically significant correlations between high-visibility "friction" events (file releases, scandals, media cycles) and institutional compliance events (policy shifts, financial positioning, regulatory changes).

**Core Finding**: Friction events (document releases, scandals) predict institutional compliance events (policy shifts, financial moves) at a 2-week lag (r = +0.6196, p = 0.0004, n = 30 weeks).

**What this means**: When high-visibility friction events spike, institutional compliance events follow ~14 days later — suggesting shared exploitation of calendar-driven attention windows.

---

## Understanding the Statistics

This research uses Pearson correlation (r) to measure relationships between event types.

| r Value | Interpretation |
|---------|----------------|
| 0.0 | No relationship |
| ±0.1-0.3 | Weak |
| ±0.3-0.5 | Moderate |
| ±0.5-0.7 | Strong |
| ±0.7-1.0 | Very strong |

**Our finding (r = +0.6196)**: When friction events spike, compliance events follow approximately 2 weeks later. This correlation (p = 0.0004) has less than 0.05% probability of occurring by chance.

**Why this matters**:
- A correlation this strong is reproducible — run the scripts in `Run_Correlations_Yourself/` yourself
- It suggests a structural pattern, not random coincidence
- Separate analyses (Project Trident, cross-validation) confirm the pattern using independent datasets

**Important caveat**: Correlation ≠ causation. We document that these events cluster together, not that one causes the other. The claim is structural: the pattern exists and is statistically significant.

---

## Key Statistics

| Finding | Value | Status |
|---------|-------|--------|
| Friction → Compliance correlation | r = +0.6196 (2-week lag) | ✅ Verified |
| Statistical significance | p = 0.0004, n = 30 weeks | ✅ Verified |
| Ritual → Policy proximity | 50.7% vs. 19.9% baseline (2.5x) | ✅ Verified |
| Project Trident significance | p = 0.002 (Mann-Whitney U) | ✅ Verified |
| Cross-validation (14-day periodicity) | χ² = 330.62 (p < 0.0001, 2,105 events) | ✅ Verified |
| December 2025 cluster | 108 events in 12-day window | ✅ Verified |
| Dec 22 signal types | 5 (Friction, Geopolitics, Financial, Policy, Cyber) | ✅ Verified |
| Event colocation | Friction dates attract 3.5x more compliance than random dates | ✅ Verified |

---

## The Convergence Model

### Original Hypothesis (Sequence)
```
Friction (t) → [creates window] → Compliance (t+14 days)
```

### Revised Finding (Convergence)
```
Calendar Anchor (solstice, holiday, fiscal deadline)
        ↓
┌───────┼───────┐
↓       ↓       ↓
Friction  Policy  Financial
        ↓
Lagged Clustering (r = 0.6196, 2-week lag)
```

The raw data shows friction and compliance events cluster together rather than following a sequential cause-effect pattern. This makes the phenomenon more robust—it doesn't require coordination, just shared exploitation of the same calendar signals.

### December 19-23, 2025: The Pincer Window

The Dec 19-23, 2025 window demonstrates convergent clustering:

| Date | Event Type | Events |
|------|-----------|--------|
| Dec 19 | Friction | Epstein Library release (DOJ) |
| Dec 19 | Financial | Bull & Bear sell signal (8.5) |
| Dec 22 | Geopolitics | China EU dairy tariffs (42.7%) |
| Dec 22 | Financial | BlackRock Bitcoin ETF "top theme" |
| Dec 22 | Cyber/Intel | CRINK nation-state threat analysis |
| Dec 22-23 | Peak | 6-8 friction + 9-13 compliance events/day |
| Dec 23 | Infrastructure | Redaction failures exposed (NYT) |

Five independent signal types converged on the same window—not because one caused another, but because all actors respond to the same environmental signals.

---

## The Three-Layer Model

This repository is part of a three-layer analytical framework:

| Layer | Repository | Focus | Primary Finding |
|-------|-----------|-------|-----------------|
| 1. Attention Capture | This repo | Friction → compliance clustering | r = 0.6196 (2-week lag) |
| 2. Vacuum Creation | DOGE_Global_Effects | Aid cuts → instability | r = 0.42-0.69, 3-12 month lag |
| 3. Alternative Capture | BRICS-NDB-LocalCurrency-DiD | Alternative financial systems | +25.5 pp local currency lending |

**Unified Thesis**: Domestic chaos consumes attention while foreign policy vacuums emerge, which alternative systems then capture.

---

## Repository Structure

```
The_Regulated_Friction_Project/
│
├── README.md                    # This file
├── Report.md                    # Executive summary and findings report
├── CITATION.cff                 # Citation metadata
├── Glossary.md                  # Key terminology definitions
├── SOURCES.md                   # 138 unique sources catalogued across all datasets
├── resistance_indicators.md     # Resistance indicator tracking
│
├── Core Analysis
│   ├── Repository_Synthesis.md                 # Three-layer framework overview
│   ├── Thermostat_Explained.md                 # Why the mechanism exists
│   ├── Claude's_Analysis.md                    # AI-assisted interpretation
│   ├── Grok_Analysis.md                        # Cross-verification with Grok
│   ├── China_State_Media_Null_and_Meanings.md  # Null finding: China state media shows no anticipatory signaling
│   └── Case_Study_David_Barnes_Detention.md    # Hostage diplomacy as human leverage dimension
│
├── December 2025 Focus
│   ├── CRUCIAL_Synthesis_Dec19_Convergence.md  # Dec 19-23 pincer window analysis
│   ├── FINANCIAL_RECEIPT_VERIFICATION.md       # Financial event verification
│   └── Main_Characters.md                      # Cabinet timing analysis
│
├── Policy & Implications
│   ├── How_This_Happened-A_Policy_Breif.md     # Regulatory citations, oversight questions
│   ├── Implications.md                         # China BRI expansion implications
│   ├── 'Transparency'_Timeline.md              # Document release history
│   └── Alternate_Mechanisms.md                 # Alternative explanations considered
│
├── Methodology & Transparency
│   ├── TRANSPARENCY_NOTE_FOR_2026_ANALYSIS.md  # Dataset inclusion/exclusion criteria
│   └── VERIFICATION_REPORT_Jan2026.md          # Complete independent statistical verification
│
├── 00_Quick_Breakdowns/                        # Executive-level summaries
│   ├── About_Me.md                              # Background on the author
│   └── Copilot_Executive_Synthesis_Feb2026.md  # Comprehensive repository synthesis (Feb 2026)
│
├── 01_Levers_and_Frictions/                    # Friction events timeline
│   ├── Epstein_Files_timeline.csv
│   └── Epstein_Files_timeline_updated.csv
│
├── 02_Anchors_and_Financials/                  # Capital flow data
│   ├── pep_banking_combined.csv
│   └── pep_banking_sentiment.csv
│
├── 03_Master_Framework/                        # Primary datasets
│   ├── MASTER_reflexive_control_2015-2025.csv
│   ├── MASTER_timeline_2015-2025_UPDATED.csv
│   └── updated_master_theory.csv
│
├── 04_Testing_and_Counters/                    # Validation datasets
│   ├── expanded_historical_backtest.csv
│   └── merged_backtest_counters.csv
│
├── 05_Geopolitical_Vectors/                    # Nation-state analysis
│   ├── CRINK_Analysis.md                              # CRINK axis integration
│   ├── Global_Election_Analysis.md                    # Allied election patterns
│   ├── Graham_Venezuela_Analysis.md                   # Graham's 54-day Venezuela escalation
│   ├── Graham_Venezuela_Posts_Timeline.csv            # Supporting timeline data
│   ├── January_2026_Parallel_Operations_Timeline.md   # Venezuela-Yemen parallel operations
│   ├── Venezuela_Privatization_Amnesty_Stack_Feb2026.md  # Venezuela compliance stack
│   └── thermostat_control_data.csv                    # Nation-state linkage data
│
├── 06_Visualizations/                          # Charts and images
│
├── 07_My_Previous_Epstein_Research/            # Pre-project archive (4 PDFs)
│
├── 08_How_It's_Possible/                       # Mechanism documentation
│   ├── 08_How_Its_Possible.md                         # Core mechanism analysis
│   ├── DOJ_Probe_Results.csv
│   ├── Phase_0_Maxwell_Pivot.csv
│   └── pincer_data.csv
│
├── 09_Silicon_Sovereignty/                     # Semiconductor, AI & infrastructure
│   ├── SILICON_SOVEREIGNTY_REPORT.md                  # Core report: compute-as-currency thesis
│   ├── Infrastructure_Consolidation_Pattern_Jan2026.md  # Oracle/MGX/PIF consortium analysis
│   ├── CRUCIAL-Cross_Verification_Check.md            # Cross-verification with llama2
│   ├── Coalition_Narrative_Map_2015-2025.csv          # Media coverage patterns (456 records)
│   ├── REFINED_supercomputer_geopolitics (1).csv      # Supercomputer geopolitics (906 records)
│   ├── Regulatory_Map_Data_CLEANED.csv                # Policy/compliance events (76 records)
│   └── VOCA_funding_timeline_clean.csv                # Victim services funding (667 records)
│
├── 10_Real-Time_Updates_and_Tasks/             # Ongoing analysis and daily tasks
│   ├── README.md
│   ├── 2026_January/                                  # January 2026 daily updates
│   ├── 2026_February/                                 # February 2026 daily updates
│   └── Tasks/                                         # Standing monitoring tasks (14 trackers)
│
├── 11_Protest_Dynamics_and_Funding/            # Protest analysis
│   ├── Protest_Funding_Audit.pdf
│   └── README.md
│
├── 12_The_Media_Firewall/                      # Media coverage patterns
│   ├── 1789_Symbolism_Analysis.md                     # 1789 Capital / Gulf SWF funding network
│   ├── Analyzing Geopolitical and Media Control.pdf
│   └── README.md
│
├── 13_State_and_County_Analysis/               # State-level forensics
│   └── arkansas_infrastructure_forensic_audit.md      # Arkansas Act 373/548, PSC analysis
│
├── Statistical Verification
│   ├── Control_Proof/                                 # Core correlation data
│   │   ├── master_reflexive_correlation_data.csv      # Weekly friction/compliance indices
│   │   ├── MASTER_reflexive_control_v2.csv
│   │   ├── reflexive_control_scraped_data.csv
│   │   ├── thermostat_control_data.csv
│   │   └── correlation_results.txt
│   │
│   ├── Run_Correlations_Yourself/                     # Independent verification suite
│   │   ├── README.md                                  # Folder guide and correlation reference
│   │   ├── requirements.txt                           # Python dependencies (pandas, numpy, scipy, statsmodels)
│   │   ├── run_original_analysis.py                   # Reproduce r = 0.6196, p = 0.002, χ² (pre-2026 data)
│   │   └── Wrong_Correlations/                        # ⚠️ Archived scripts that used wrong datasets or excluded data
│   │       ├── README.md                              # Explanation of what went wrong
│   │       ├── reproduce_updated_correlation.py       # (used 2025-only datasets inflating correlation to r = 0.6685)
│   │       ├── original_correlation_test.py           # (used relative paths — was correct)
│   │       ├── reproduce_original_correlation.py      # (used hardcoded paths to wrong datasets)
│   │       ├── independent_statistical_verification.py # (used hardcoded paths to wrong datasets)
│   │       ├── run_original_analysis.py               # (was correct — archived copy)
│   │       └── DISCREPANCY_ANALYSIS.md                # Methodology comparison (still valid)
│   │
│   └── Project_Trident/                               # Temporal correlation study
│       ├── PROJECT_TRIDENT_CASE_STUDY.md
│       ├── The_Trident.md                             # Three-prong mechanism
│       ├── DATASET_REFERENCE.md
│       ├── Veriify_Trident_Analysis.py                # Verify ritual timing analysis
│       ├── anchor_events_parsed.csv                   # 70 anchor events
│       ├── project_trident_final_dossier.csv          # 118 dossier entries
│       ├── ritual_events_parsed.csv                   # 51 ritual events
│       ├── temporal_correlations_analyzed.csv          # 338 temporal pairings
│       ├── Best_Data_For_Project_Trident/             # Ritual timing, fund flow datasets (8 files)
│       ├── Claude_Code_Analysis/                      # Q1 2026 Privatized Integration research
│       │   ├── Privatized_Integration_Networks_Q1_2026_Synthesis.md  # Master document
│       │   ├── Phoenix_Settlement_Portfolio_and_New_Gaza.md          # Reference appendix
│       │   ├── LEAD_ANALYST_REVIEW.md                               # Independent verification
│       │   └── README.md
│       └── Copilot_Opus_4.6_Analysis/                 # Lead Researcher statistical verification
│           ├── README.md                              # Transparency notice, methodology, work log
│           ├── Statistical_Tests/                     # 9 runnable Python robustness scripts
│           ├── Findings/                              # Active analysis — provenance, backfill guide
│           ├── Verification_Reports/                  # Prediction tracker
│           ├── Consolidation_Analysis/                # Cross-domain consolidation assessment
│           ├── Archive/                               # Previous analysis kept for transparency
│           └── Datasets/                              # Local copies of original pre-2026 CSVs (19 files)
│
└── New_Data_2026/                              # January-February 2026 datasets
    ├── 2026_Analysis.md                               # Correlation methodology and findings
    ├── Additional_Anchors_Jan2026_Final.csv
    ├── Biopharma.csv
    ├── BlackRock_Timeline_Full_Decade.csv
    ├── CRINK_Intelligence_Dataset_Final_Verified.csv
    ├── High_Growth_Companies_2015_2026.csv
    ├── Infrastructure_Forensics.csv
    └── Timeline_Update_Jan2026_Corrected (1).csv
```

---

## What's New (v8.3 - February 2026)

### Correlation Correction & Robustness Verification

v8.3 corrects the correlation statistics throughout the README and Report to match the verified findings from the `Copilot_Opus_4.6_Analysis/` robustness audit. The January 2026 analysis had inadvertently used the wrong datasets for robustness testing (New_Data_2026 files instead of the original pre-2026 datasets). All robustness tests have been re-run against the correct original datasets.

### 1. Corrected Robustness Findings

The original correlations (r = 0.6196) remain valid using the pre-2026 datasets. The previously reported r = 0.6685 and r = 0.5268 (from New_Data_2026) have been deprecated because those datasets included 2025-only data that inflated the correlations. The key correction is to the **robustness story**:

| Test | Previous (Wrong Datasets) | Corrected (Original Datasets) |
|------|--------------------------|-------------------------------|
| Dec 2025 exclusion | 90% drop, not significant | 29% drop, still significant (p < 0.0001) |
| Autocorrelation adjustment | Mixed | Both Pearson and Spearman survive (p < 0.001) |
| Normalized (binary) | Negative | Positive (r = 0.36) |
| Event-study | Not tested | Colocation confirmed (40-60x random baseline) |
| Granger causality (30-row) | Not tested | Friction → Compliance at lags 1-2 (p = 0.0008) |
| Granger causality (event counts) | Not tested | Bidirectional — suggests common driver |

**Key improvement:** The signal is distributed across the full 1990–2025 timeline, not concentrated in a single month. Removing December 2025 only reduces the original-dataset correlation by 29% (previously reported as 90% with wrong datasets).

### 2. New Subfolder: `Project_Trident/Copilot_Opus_4.6_Analysis/`

Lead Researcher verification suite maintained by GitHub Copilot (Claude, Opus 4.6). Contains:

- **9 runnable Python scripts** — permutation tests, autocorrelation adjustment, normalized correlation, Dec 2025 cross-validation, rolling-window analysis, event-study framework, Granger causality
- **5 findings documents** — dataset provenance, correlation summary, robustness test results, Granger causality results, backfill recommendations
- **1 scrutiny report** — independent verification of all scripts and factual claims
- **19 dataset copies** — local copies of original pre-2026 CSVs for reproducibility

### 3. Ritual Proximity Ratio Correction

Corrected the ritual → policy proximity ratio from 3.5x to **2.5x** (50.7% / 19.9% = 2.55x). The previous 3.5x was a calculation error.

### 4. README Structure Updates

Added previously undocumented files to the Repository Structure:
- `00_Quick_Breakdowns/About_Me.md`
- `resistance_indicators.md`
- `Project_Trident/` CSV files (anchor_events_parsed, project_trident_final_dossier, ritual_events_parsed, temporal_correlations_analyzed)
- Full `Project_Trident/Copilot_Opus_4.6_Analysis/` subfolder tree

---

## Quick Navigation by Type

### Datasets
- `Control_Proof/master_reflexive_correlation_data.csv` — Core friction/compliance data
- `New_Data_2026/` — January-February 2026 updates (8 datasets)
- `05_Geopolitical_Vectors/thermostat_control_data.csv` — Nation-state linkages
- `Project_Trident/Best_Data_For_Project_Trident/` — Ritual timing, fund flows

### Statistical Verification
- `Run_Correlations_Yourself/run_original_analysis.py` — Reproduce original r = 0.6196, p = 0.002, χ² (pre-2026 data)
- `Run_Correlations_Yourself/Wrong_Correlations/` — ⚠️ Archived scripts that used wrong datasets or excluded data (kept for transparency)
- `Project_Trident/Veriify_Trident_Analysis.py` — Verify ritual timing analysis
- `Project_Trident/Copilot_Opus_4.6_Analysis/Statistical_Tests/` — 9 robustness test scripts (permutation, autocorrelation, normalization, Dec 2025 exclusion, rolling window, event-study, Granger causality)
- `Project_Trident/Copilot_Opus_4.6_Analysis/Findings/dataset_provenance.md` — Dataset provenance documentation

### Deep Dives by Topic
- **Tech Infrastructure**: `09_Silicon_Sovereignty/SILICON_SOVEREIGNTY_REPORT.md`
- **Infrastructure Consolidation**: `Project_Trident/Copilot_Opus_4.6_Analysis/Consolidation_Analysis/consolidation_pattern_significance.md`
- **Privatized Integration**: `Project_Trident/Claude_Code_Analysis/Privatized_Integration_Networks_Q1_2026_Synthesis.md`
- **State Regulatory Capture**: `13_State_and_County_Analysis/arkansas_infrastructure_forensic_audit.md`
- **Geopolitical Shifts**: `05_Geopolitical_Vectors/` (Venezuela, Yemen, CRINK, allied elections)
- **Media Funding Networks**: `12_The_Media_Firewall/1789_Symbolism_Analysis.md`

---

## For Researchers

### Start Here
1. `Repository_Synthesis.md` — Three-layer framework overview
2. `New_Data_2026/2026_Analysis.md` — Latest correlation findings
3. `Project_Trident/Claude_Code_Analysis/Privatized_Integration_Networks_Q1_2026_Synthesis.md` — Q1 2026 applied findings
4. `13_State_and_County_Analysis/arkansas_infrastructure_forensic_audit.md` — State-level pattern

### Verify the Statistics
```bash
# Install dependencies
cd Run_Correlations_Yourself/
pip install -r requirements.txt

# Reproduce original correlations (pre-2026 datasets)
python run_original_analysis.py              # r = 0.6196, p = 0.002, χ² cross-validation

# Run robustness tests (from repo root)
cd ../Project_Trident/Copilot_Opus_4.6_Analysis/Statistical_Tests/
python permutation_test.py                   # Shuffle-based significance
python autocorrelation_adjusted_test.py      # Block bootstrap
python cross_validation_dec2025.py           # Dec 2025 exclusion test
python granger_causality_test.py             # Predictive direction test
```

### Key Datasets
- `Control_Proof/master_reflexive_correlation_data.csv` — Weekly friction/compliance indices
- `Project_Trident/Best_Data_For_Project_Trident/ritual_events_parsed.csv` — Project Trident ritual timing
- `New_Data_2026/CRINK_Intelligence_Dataset_Final_Verified.csv` — CRINK axis discourse tracking
- `09_Silicon_Sovereignty/VOCA_funding_timeline_clean.csv` — Victim services funding

---

## For Policymakers & Journalists

### Start Here
1. `How_This_Happened-A_Policy_Breif.md` — Regulatory citations, oversight questions
2. `Project_Trident/Claude_Code_Analysis/Privatized_Integration_Networks_Q1_2026_Synthesis.md` — Board of Peace, Affinity/Phoenix, MEAD-CDOC
3. `13_State_and_County_Analysis/arkansas_infrastructure_forensic_audit.md` — State-level regulatory capture
4. `05_Geopolitical_Vectors/Venezuela_Privatization_Amnesty_Stack_Feb2026.md` — Compliance reset pattern

### Key Questions Raised
- Why did the PSC approve a $1.5B project it explicitly found "not reasonable"?
- Why did TikTok censorship reports emerge 72 hours after Oracle/UAE consortium takeover?
- Why did major Saudi-UAE rupture occur during Venezuela media saturation?
- Why do the same entities appear in EA, TikTok, Stargate, Grok, and World Liberty Financial deals?
- Why has AVAIO's $750M anchor investor remained undisclosed for 5 years?

### Testable Predictions

| Prediction | Timeframe | Status |
|-----------|-----------|--------|
| Event clustering at next file deadline | Ongoing | ✅ Confirmed (Jan 30-Feb 1) |
| Tu BiShvat policy action | Feb 12, 2026 | Pending |
| Gulf SWF Q4 positioning revealed | Feb 2026 | Pending (13F filings) |
| DOGE-predicted instability | Q1 2026 | Tracking (Mali, Syria, Sudan) |
| California TikTok investigation findings | Q1 2026 | Pending |
| Khanna investigation findings | March 2026 | Document deadline March 1 |
| UK Mandelson disclosure | Feb-March 2026 | Parliamentary vote passed |
| Arkansas PSC order text release | Q1 2026 | FOIA pending |

---

## Methodology

1. **Multi-AI Verification**: Findings cross-checked using Claude, Grok, and Gemini
2. **Statistical Testing**: Pearson correlation, Mann-Whitney U, chi-square, Granger causality, permutation tests
3. **Robustness Testing**: Autocorrelation adjustment, Dec 2025 exclusion, normalized correlation, rolling-window analysis, event-study framework (see `Project_Trident/Copilot_Opus_4.6_Analysis/`)
4. **Raw Event Counts**: Replaced subjective scoring with verifiable event counts
5. **Source Triangulation**: Government filings, financial data, news archives
6. **Cross-Repo Validation**: Patterns verified across three independent datasets
7. **Explicit Limitations**: Documented in each module

---

## Limitations & Disclaimer

This repository documents **correlations, not causation**. All findings derive from publicly available data using standard statistical methods.

**The author makes no claims about**:
- Intent or coordination between actors
- Individual motivations or culpability
- Whether patterns are deliberate or emergent

**The claim is structural**: Statistically significant clustering patterns exist and are reproducible.

The "Main Characters," "Implications," and state-level analysis modules specifically disclaim any assertion of conscious coordination. Performative patterns enable detection of quieter correlations—this is an analytical observation, not an accusation.

---

## Connected Repositories

| Repository | Focus |
|-----------|-------|
| **DOGE_Global_Effects** | Aid cuts → instability mapping |
| **BRICS-NDB-LocalCurrency-DiD** | Alternative financial systems |
| **Project-Chrysanthemum_Japan-China-AI** | Japan-China tech integration |
| **Sovereign-Capital-Audit** | Gulf SWF positioning |

---

## Statistical Validation

Core findings independently verified January–February 2026:
- **Original correlation** (r = 0.6196, 2-week lag): ✅ Exact reproduction
- **Project Trident** (p = 0.002): ✅ Exact reproduction
- **Ritual proximity** (50.7% vs 19.9%, 2.5x): ✅ Exact reproduction
- **Cross-validation** (χ² = 330.62): ✅ Exact reproduction
- **December 2025 anomaly**: ✅ Confirmed (z = 2.35, p < 0.01)

**Note:** The previously reported r = 0.6685 and r = 0.5268 (from New_Data_2026) have been deprecated. Those correlations used 2025-only datasets that inflated the results. The archived scripts are in `Run_Correlations_Yourself/Wrong_Correlations/` for transparency.

### Robustness Tests (Copilot_Opus_4.6_Analysis, Feb 2026)

Using the original pre-2026 datasets plus newly incorporated data from folders 01, 02, 03:
- **Permutation test (30-row)**: r = 0.62 significant (p < 0.001, 1K shuffles)
- **Permutation test (multi-dataset)**: Spearman ρ = 0.61 significant (p < 0.0001, 10K shuffles)
- **Granger causality (30-row)**: Friction → Compliance at lags 1-2 (p = 0.0008)

See `VERIFICATION_REPORT_Jan2026.md` and `Project_Trident/Copilot_Opus_4.6_Analysis/` for complete independent analyses.

---

## Contact

**GitHub**: [@Leerrooy95](https://github.com/Leerrooy95)

**Last updated**: February 9, 2026 — Corrected primary finding to r = 0.6196 (original analysis), deprecated r = 0.6685 (used 2025-only datasets), incorporated datasets from folders 01-03
