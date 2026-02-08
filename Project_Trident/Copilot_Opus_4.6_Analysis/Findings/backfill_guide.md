# Dataset Backfilling Guide

**Purpose:** Help even out CSV datasets that are heavily skewed toward 2025 by adding legitimate, source-verified historical data for earlier years.

**Date:** February 2026

---

## The Problem

The year distribution audit (`year_distribution_audit.py`) found that 2025 accounts for 29.6% of all events across the repository — **4.7× the 2015–2024 average** of 389 events/year.  The BlackRock timeline (~60 events/year, evenly distributed) shows what a well-balanced dataset looks like.

### Datasets That Need Backfilling

| File | Current 2025% | Missing Years | Categories to Fill |
|------|---------------|---------------|--------------------|
| **Biopharma.csv** | 73.8% (79/107) | 2015–2022 | Conflict, Corporate, FDA_Reg, Policy, Funding |
| **Infrastructure_Forensics.csv** | 100% (102/102) | 2015–2024 | Legislation, Ritual_Event, Political_Org, Federal_Contract |
| **CRINK_Intelligence_Dataset_Final_Verified.csv** | 97.1% (33/34) | 2015–2024 | Analysis, Military_Security, Cyber_Security |
| **Additional_Anchors_Jan2026_Final.csv** | 96.0% (48/50) | 2015–2024 | Geopolitics, Policy, Ritual_Event |

### Datasets That Are Already Balanced (No Changes Needed)

| File | 2025% | Status |
|------|-------|--------|
| **BlackRock_Timeline_Full_Decade.csv** | 9.5% | ✓ Reference model |
| **High_Growth_Companies_2015_2026.csv** | 12.7% | ✓ Balanced |
| **MASTER_timeline_2015-2025_UPDATED.csv** | 11.6% | ✓ Balanced |

---

## Why AI Cannot Backfill This Data Directly

The datasets in this repository contain **scraped, source-verified events** with real URLs.  Backfilling requires:

1. **Real events** that actually happened on specific dates
2. **Real source URLs** that can be verified
3. **Accurate snippets** from those sources
4. **Correct category classification** matching the existing taxonomy

An AI model can identify *what kinds of events* to search for, but should not fabricate specific dates, URLs, or snippets — that would undermine the repository's credibility.  The user should scrape or manually verify each entry.

---

## Backfilling Strategies Per Dataset

### 1. Biopharma.csv

**Current coverage:** 2023–2026 (mostly Neuralink/FDA)
**Target:** Add ~10–15 events per year for 2015–2022
**Column format:** `date,event,category,source_url,correlation_value`

**Search queries for historical data:**

| Year Range | Category | Suggested Search Queries |
|-----------|----------|-------------------------|
| 2015–2017 | FDA_Reg | `"FDA drug approval" controversy [year]`, `"FDA device approval" brain implant [year]` |
| 2015–2017 | Conflict | `biopharma regulation conflict Congress [year]`, `FDA commissioner conflict interest [year]` |
| 2015–2017 | Corporate | `biopharma merger acquisition [year]`, `pharmaceutical corporate restructuring [year]` |
| 2015–2017 | Policy | `biopharma policy reform [year]`, `drug pricing legislation [year]` |
| 2015–2017 | Funding | `NIH funding biopharma [year]`, `DARPA brain research funding [year]` |
| 2018–2020 | FDA_Reg | `"Aduhelm" FDA approval controversy`, `COVID vaccine EUA FDA [year]` |
| 2018–2020 | Conflict | `Purdue Pharma opioid crisis [year]`, `FDA opioid regulation conflict [year]` |
| 2021–2022 | FDA_Reg | `Biogen Aduhelm FDA investigation 2022`, `Neuralink FDA application rejection 2022` |
| 2021–2022 | Policy | `Build Back Better drug pricing 2021`, `Inflation Reduction Act drug negotiation 2022` |

**Key verified events to include:**

- 2016: Sarepta Exondys 51 approved against advisory panel (FDA_Reg)
- 2017: FDA commissioner Scott Gottlieb appointed, deregulation push (Policy)
- 2018: FDA approves first cannabis-derived drug Epidiolex (FDA_Reg)
- 2019: Purdue Pharma files bankruptcy amid opioid crisis (Conflict)
- 2020: COVID-19 EUA process debate — speed vs safety (Conflict)
- 2021: FDA approves Biogen Aduhelm against advisory panel, congressional probe (FDA_Reg)
- 2022: FDA rejects Neuralink's first human trial application (FDA_Reg)
- 2022: Inflation Reduction Act — Medicare drug price negotiation (Policy)

---

### 2. Infrastructure_Forensics.csv

**Current coverage:** 2025 only (all December 2025 events)
**Target:** Add ~8–10 events per year for 2015–2024
**Column format:** `date,event,category,snippet,source_url`

**Search queries:**

| Year Range | Category | Suggested Search Queries |
|-----------|----------|-------------------------|
| 2015–2017 | Legislation | `federal infrastructure bill [year]`, `highway bill reauthorization [year]` |
| 2015–2017 | Federal_Contract | `federal infrastructure contract award [year]`, `DOT contract [year]` |
| 2018–2020 | Legislation | `infrastructure week Trump [year]`, `FAST Act implementation [year]` |
| 2021–2022 | Legislation | `"Infrastructure Investment and Jobs Act" 2021`, `"CHIPS Act" 2022` |
| 2023–2024 | Federal_Contract | `IIJA project awards [year]`, `broadband infrastructure grants [year]` |
| 2015–2024 | Political_Org | `US Chamber of Commerce infrastructure lobbying [year]` |

**Key verified events:**

- 2015-12-04: FAST Act signed ($305B highway/transit, 5-year authorization) (Legislation)
- 2018-02-12: Trump $1.5T infrastructure plan released, stalls in Congress (Legislation)
- 2021-08-10: Infrastructure Investment and Jobs Act passes Senate (Legislation)
- 2021-11-15: IIJA signed into law — $1.2T including $550B new spending (Legislation)
- 2022-08-09: CHIPS and Science Act signed — $52.7B semiconductors (Legislation)
- 2022-08-16: Inflation Reduction Act signed — climate/energy infrastructure (Legislation)
- 2023-onwards: IIJA grant awards rolling out (Federal_Contract)

---

### 3. CRINK_Intelligence_Dataset_Final_Verified.csv

**Current coverage:** 2025–2026 only
**Target:** Add ~3–5 events per year for 2015–2024
**Column format:** `date,event,category,snippet,source,link`

**Search queries:**

| Year Range | Category | Suggested Search Queries |
|-----------|----------|-------------------------|
| 2015–2017 | Cyber_Security | `Russia cyber attack US [year]`, `China OPM hack 2015`, `North Korea Sony hack` |
| 2015–2017 | Military_Security | `Russia Crimea military [year]`, `China South China Sea [year]`, `Iran nuclear deal [year]` |
| 2018–2020 | Cyber_Security | `SolarWinds hack Russia 2020`, `Iran cyber attack [year]`, `North Korea WannaCry 2017` |
| 2018–2020 | Analysis | `CRINK threat assessment [year]`, `US intelligence community threat report [year]` |
| 2021–2024 | Military_Security | `Russia Ukraine invasion 2022`, `China Taiwan military [year]`, `Iran proxy attacks [year]` |
| 2021–2024 | Cyber_Security | `Colonial Pipeline ransomware 2021`, `China Volt Typhoon 2023` |

**Key verified events:**

- 2015-06-04: China OPM hack — 21.5M federal employee records stolen (Cyber_Security)
- 2017-05-12: WannaCry ransomware — attributed to North Korea (Cyber_Security)
- 2020-12-13: SolarWinds hack disclosed — attributed to Russia (Cyber_Security)
- 2021-05-07: Colonial Pipeline ransomware attack — Russia-linked (Cyber_Security)
- 2022-02-24: Russia invades Ukraine (Military_Security)
- 2023-05-24: Volt Typhoon — China-linked infiltration of US infrastructure (Cyber_Security)
- 2024: Iran-backed proxy attacks escalate in Middle East (Military_Security)

---

### 4. Additional_Anchors_Jan2026_Final.csv

**Current coverage:** 2025–2026 (Dec 2025 events)
**Target:** Add ~5–8 events per year for 2015–2024
**Column format:** `date,event,category,snippet,source_url`

**Search queries:**

| Year Range | Category | Suggested Search Queries |
|-----------|----------|-------------------------|
| 2015–2024 | Geopolitics | `US geopolitical event [year]`, `NATO expansion [year]`, `trade war [year]` |
| 2015–2024 | Policy | `US domestic policy shift [year]`, `executive order significant [year]` |

**Key verified events:**

- 2015-07-14: Iran nuclear deal (JCPOA) finalized (Geopolitics)
- 2016-11-08: Trump elected — geopolitical realignment begins (Geopolitics)
- 2018-03-22: US-China trade war tariffs begin (Geopolitics)
- 2019-10-06: US withdraws troops from northern Syria (Geopolitics)
- 2020-01-03: US kills Iranian General Soleimani (Geopolitics)
- 2021-08-30: US completes Afghanistan withdrawal (Geopolitics)
- 2022-02-24: Russia-Ukraine conflict escalates (Geopolitics)
- 2023-10-07: Hamas attack on Israel — regional realignment (Geopolitics)

---

## How to Backfill

### Step-by-step process:

1. **Pick a dataset** from the table above
2. **Use the suggested search queries** in Google/Bing to find real events
3. **For each event, record:**
   - `date` — exact date in YYYY-MM-DD format
   - `event` — brief description matching the existing style
   - `category` — use ONLY the categories already in that CSV
   - `snippet` — copy a sentence from the source article
   - `source_url` — the actual URL you found it at
4. **Aim for even distribution:** ~5–15 events per year, similar to the BlackRock reference
5. **Verify every URL** before adding — dead links reduce credibility

### Validation:

After backfilling, run the year distribution audit to check your work:

```bash
python3 Project_Trident/Copilot_Opus_4.6_Analysis/Statistical_Tests/year_distribution_audit.py
```

A well-balanced dataset should show each year within 2× of the average. The BlackRock file is the gold standard — note how it ranges from 54 to 67 events per year (very consistent).

---

## Target Distribution

For a dataset covering 2015–2025 (11 years), aim for:

| Quality Level | Events/Year | Variation |
|--------------|-------------|-----------|
| Excellent (BlackRock-level) | 50–70 | ±15% |
| Good | 30–50 | ±25% |
| Acceptable | 10–20 | ±40% |
| Problematic | <5 some years, >50 others | >100% |

---

*Created by year distribution audit analysis, February 2026*
