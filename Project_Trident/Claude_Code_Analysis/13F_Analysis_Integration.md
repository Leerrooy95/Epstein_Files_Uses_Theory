# 13F Analysis Integration — Apollo Credit Pipeline and Q4 Verification Framework

## Transparency Notice
**This analysis was produced by Claude Code (Lead Analyst, Claude_Code_Analysis subfolder).** It integrates findings from the Copilot_Opus_4.6_Analysis/13F_Analysis files (dated February 14, 2026) with the existing Claude_Code_Analysis synthesis documents. All claims are sourced from publicly available SEC filings, verified news reporting, and the cross-referenced analyses below. Treat as analysis to be verified, not established fact.

---

**Analyst:** Claude Code (Lead Analyst)
**Date:** February 14, 2026
**Integrating:**
- `13F_Verification_Report_Feb14_2026.md` (Copilot main 13F analysis)
- `13F_Supplementary_Analysis_Feb14_2026.md` (Apollo credit pipeline discovery)
- `13F_Holdings_Baseline_Q3_2025.csv` (Raw Q3 holdings data)
- `Entity_13F_Cross_Reference.csv` (Entity tier assignments)
- `Security_Level_Cross_Reference.csv` (Security-level cross-entity analysis)
**Cross-referenced against:**
- `Pre_13F_Verification_Baseline.md` (Claude Code, Feb 13)
- `Privatized_Integration_Networks_Q1_2026_Synthesis.md` (Master document)
- `Phoenix_Settlement_Portfolio_and_New_Gaza.md` (Reference appendix)
- `LEAD_ANALYST_REVIEW.md` (Running review log)

---

## 1. Structural Finding: Apollo as Credit Backbone

### 1A. The Analytical Error and Its Correction

The Pre_13F_Verification_Baseline (Feb 13) classified Apollo as a standard entity to watch for "infrastructure/reconstruction-adjacent positions" in its 13F portfolio. The Copilot 13F analysis initially confirmed this lens — Apollo's Q3 2025 13F shows insurance (Aspen, $2.77B), security (ADT, $888M), and hospitality (Hilton Grand Vacations, $763M). The initial assessment: TIER 2 — MODERATE.

This was the wrong analytical frame. The Supplementary Analysis (Feb 14) correctly identifies that Apollo's role in the framework is **debt/financing, not equity**. Apollo's 13F is structurally irrelevant to understanding its position because credit facilities, term loans, and debt arrangements do not appear in 13F filings.

**Revised assessment: TIER 1 — CRITICAL.**

### 1B. Apollo Credit Pipeline — Verified Positions

| Recipient | Apollo Credit Role | Amount | Date | Verification |
|---|---|---|---|---|
| QXO (Affinity Partners' sole 13F holding) | Led $1.2B convertible preferred | $1.2B | Jan 2026 | EquipmentFinanceNews, ainvest.com |
| QXO (with Temasek) | Led additional $1.8B financing | $1.8B | Jan 2026 | USNews, GlobalBankingandFinance |
| xAI (Valor Compute) | Led $3.5B capital solution for data center compute | $3.5B | Jan 2026 | Apollo press release, AlternativesWatch |
| Meta | Lead structurer/co-lender for data center expansion | Up to $29B | 2025-2026 | DataCenterDynamics, TradingAlgo |
| Stream Data Centers | Acquired majority stake | Undisclosed (billions) | Aug-Nov 2025 | Apollo press release |

**Total verified credit pipeline: $37.5B+ across five entities.**

Apollo's reported metrics (Q4 2025 earnings, Feb 9, 2026):
- Total AUM: ~$1 trillion
- Credit as % of AUM: ~82% ($690B+)
- 2025 total origination: $305B+ ($282B debt)
- Digital infrastructure deployed 2022-2025: $38-40B

### 1C. The Apollo-QXO-Affinity Triangle

This is the most structurally significant finding in the 13F integration. Three entities form a documented capital chain:

```
Gulf SWF Capital (PIF $2B, QIA, UAE)
            |
    Affinity Partners (Kushner) --- 13F: 100% in QXO ($623M)
            |
    QXO Inc ($11B Beacon + $2.25B Kodiak) --- Building products consolidation
            |
    Apollo Global ($3.0B credit to QXO in Jan 2026 alone)
            |
    Marc Rowan --- Board of Peace Executive Board + Apollo CEO
```

**What this means:**
- Affinity holds 100% of its public portfolio in QXO
- Apollo provides $3.0B in credit financing to QXO (Jan 2026)
- Temasek (Singapore SWF) co-leads the $1.8B tranche
- QXO uses this capital to consolidate US building products distribution ($50B revenue target)
- Marc Rowan sits on the Board of Peace Executive Board AND runs the credit pipeline

The governance-to-financing pipeline runs: Board of Peace governance role (Rowan) → Apollo credit capacity ($690B+) → QXO building materials consolidation (Affinity) → Gulf SWF capital origin (PIF/QIA).

### 1D. Apollo-xAI-Gulf Connection

The $3.5B Valor Compute/xAI credit deal connects to the framework through:
- xAI's $20B Series E investors include **QIA (Qatar)** and **MGX (Abu Dhabi/Tahnoon)**
- 1789 Capital portfolio includes xAI exposure
- Structure: Triple net lease — xAI leases NVIDIA GB200 GPUs; NVIDIA is anchor LP in Valor Compute
- Apollo provides the debt backbone for AI compute infrastructure used by Gulf-invested entities

### 1E. Where Apollo Fits in the Updated Actor Map

**Previous actor mapping** (from Privatized_Integration_Networks Synthesis, Part VII):

| Entity | Board of Peace | Phoenix/Affinity | TikTok | EA | MEAD-CDOC |
|---|---|---|---|---|---|
| Saudi PIF | Signatory | LP ($2B) | -- | 93.4% | Red Sands |
| UAE/MGX | Signatory | LP | 15% | -- | CAOC member |
| Oracle | -- | -- | 15% | -- | -- |
| Silver Lake | -- | -- | 15% | 5.5% | -- |
| Kushner | Executive Board | CEO, Affinity | -- | 1.1% | -- |
| Gabay | Gaza Exec Board | Bank Leumi bg | -- | -- | -- |

**Updated mapping — adding Apollo credit layer:**

| Entity | Board of Peace | Phoenix/Affinity | TikTok | EA | MEAD-CDOC | **Credit/Debt** |
|---|---|---|---|---|---|---|
| Saudi PIF | Signatory | LP ($2B) | -- | 93.4% | Red Sands | -- |
| UAE/MGX | Signatory | LP | 15% | -- | CAOC member | xAI $20B Series E (QIA+MGX) |
| Oracle | -- | -- | 15% | -- | -- | -- |
| Silver Lake | -- | -- | 15% | 5.5% | -- | -- |
| Kushner | Executive Board | CEO, Affinity | -- | 1.1% | -- | QXO (sole 13F position) |
| Gabay | Gaza Exec Board | Bank Leumi bg | -- | -- | -- | -- |
| **Apollo/Rowan** | **Executive Board** | -- | -- | -- | -- | **QXO $3B, xAI $3.5B, Meta $29B, Stream DC** |
| **Temasek** | -- | -- | -- | -- | -- | **QXO $1.8B co-lead** |

Apollo fills the previously empty "Credit/Debt" column. No other tracked entity provides this function at this scale. Marc Rowan is the only individual who bridges both the governance layer (Board of Peace Executive Board) and the credit infrastructure layer (Apollo's $690B+ credit book).

---

## 2. 13F Visibility Gap — Confirmed Architecture

### 2A. What IS Visible in 13F (Q3 2025 Baseline)

| Entity | Key 13F Positions | Total Value | Tier |
|---|---|---|---|
| PIF | EA ($3.96B, 9.9%), Uber ($6.8B), TTWO ($2.77B), Lucid ($3.74B) | ~$19.4B | TIER 1 |
| Mubadala | GlobalFoundries ($16.14B, 81.1%), ARM ($213M), LMT ($9.26M, NEW) | ~$17.9B | TIER 1 |
| Silver Lake | Unity ($1.39B), Klarna ($530M, NEW), N-able ($480M) | ~$5.13B | TIER 1 |
| Affinity Partners | QXO ($623M, 100% of portfolio) | $623M | TIER 1+ |
| Apollo | Aspen ($2.77B), ADT ($888M), HGV ($763M) | ~$9.12B | TIER 1 (upgraded) |
| QIA | GBTG (16.6%), Vistra (5.5%, reduced), ALHC (6.69%) | Unknown | TIER 2 |

### 2B. What IS NOT Visible (Confirmed 13F-Invisible)

| Arrangement | Reason 13F-Invisible | Value (if known) |
|---|---|---|
| Affinity → Phoenix Financial (9.9%) | TASE-listed, not US exchange | ~$300M+ est. |
| 1789 Capital → Anduril, Vulcan Elements, Skild AI | All private companies | $2B+ AUM |
| MGX → TikTok USDS (15%), OpenAI, xAI, Mistral | All private investments/JVs | Multi-billion |
| EA acquisition (post-close) | Going private after deal | $55B |
| Silver Lake → TikTok USDS (15%) | Private JV structure | ~$2.1B |
| ADQ → ECP $25B partnership | Private partnership | $25B |
| Gulf SWF → LP stakes in US PE/VC | CFIUS Section 800.307 passive LP exemption | Unknown |
| Apollo → QXO credit ($3B) | Credit facilities not 13F-eligible | $3B |
| Apollo → xAI credit ($3.5B) | Credit facilities not 13F-eligible | $3.5B |
| Apollo → Meta credit ($29B) | Credit facilities not 13F-eligible | Up to $29B |
| Apollo → Stream Data Centers | Private equity/credit | Billions |

**Estimated 13F-invisible capital: $120B+**
**Estimated 13F-visible capital: ~$52B**

This ratio (~70% invisible) confirms the Pre_13F_Verification_Baseline's structural prediction: "the architecture operates in 13F-invisible structures." The Supplementary Analysis adds the critical Apollo credit layer, which accounts for $37.5B+ of the invisible total.

### 2C. Connection to Project Trident Prong 2

The 13F visibility gap is a live demonstration of **Prong 2 (Regulatory Exemptions)** from the Trident framework:

| Exemption Mechanism | Application Found |
|---|---|
| CFIUS Section 800.307 (passive LP) | Gulf SWF → Affinity Partners LP relationship |
| Non-US exchange (TASE) | Phoenix Financial invisible to 13F |
| Private company/JV | TikTok USDS, OpenAI, xAI, Anduril, Mistral |
| Credit (not equity) | Apollo's entire $37.5B+ pipeline |
| Going-private transactions | EA post-close removes from 13F universe |
| Below-threshold structuring | 1789 Capital — $2B AUM, no 13F |

The Lawfare CFIUS analysis (Oct 2025) documented the political dimension: Affinity's 1.1% EA stake as "safe harbor" from CFIUS review. The 13F data now confirms the structural dimension: the architecture is designed so that the most consequential capital flows operate in regulatory blind spots.

---

## 3. Q4 2025 Verification Targets (February 17, 2026+)

### 3A. Priority 1 — Immediate Checks When Filings Drop

| Target | What to Check | Q3 Baseline | Significance |
|---|---|---|---|
| PIF Q4 2025 | EA position: any change from 24,807,932 shares? | $3.96B, 9.9% | Pre-close accumulation would signal consortium coordination timing |
| PIF Q4 2025 | Any NEW positions in Oracle, defense, or AI infrastructure? | 0 positions in these sectors | Would confirm "December pincer window" sector positioning |
| PIF Q4 2025 | Portfolio count: still 6, or re-expanded? | Slashed from 57 to 6 in Q3 | Where did exited capital go? Private transactions? |
| Mubadala Q4 2025 | LMT position: increase from 18,554 shares? | $9.26M (NEW in Q3) | Defense rotation continuation |
| Mubadala Q4 2025 | Any NEW Oracle, AMD, NVIDIA positions? | 0 in compute layer | Would indicate Pax Silica sector alignment |
| Silver Lake Q4 2025 | Does EA appear as formal position? | Not in Q3 (deal announced end of Q3) | 5.5% consortium stake should materialize |
| Affinity Q4 2025 | Still 100% QXO? Position size change? | $623M sole holding | Reduction would indicate capital redeployment elsewhere |

### 3B. Priority 2 — New Entity Search

| Target | What to Look For | Current Status |
|---|---|---|
| 1789 Capital | First-time 13F filing; fund closed at $2B year-end | No 13F exists; Form D only |
| MGX | First-time 13F filing; any US-listed AI/tech positions | No 13F exists; all private |
| Colombier III (CLBR) | Institutional 13F holders of SPAC | IPO Feb 2026; too new for Q4 data |
| ADQ investment arms | ECP partnership positions; data center/energy | Separate CIKs; not fully mapped |

### 3C. Priority 3 — Pattern Verification

| Pattern | What It Would Show | Q3 Baseline |
|---|---|---|
| Oracle (ORCL) new Gulf SWF entries | "Data custody" layer becoming visible | No Gulf SWF in Q3; only Norges Bank (+9M shares) |
| Cross-entity clustering: 2+ entities in same security | Coordination or convergent thesis | Only Klarna overlap (Mubadala + Silver Lake) in Q3 |
| Defense sector entries across Gulf SWFs | Pax Silica defense integration positioning | Only Mubadala LMT ($9.26M) in Q3 |
| "Beard" entities in Oracle/PLTR/LHX top holders | Sovereign capital routing via generic LLCs | No obvious beards found in Q3; Saiph Capital LLC flagged (weak signal) |
| Apollo 13F changes | Any new positions in tracked securities | Insurance/hospitality dominated Q3 |

### 3D. Disconfirmation Criteria (Updated)

From the Pre_13F_Verification_Baseline, updated with Q3 results:

| Criterion | Q3 Status | Q4 Will Show |
|---|---|---|
| No Gulf SWF increases in Oracle/defense/AI | Q3: No Oracle/AI; tiny LMT only | **Definitive test** — Q4 covers the window |
| 1789 Capital portfolio doesn't align with Pax Silica | Can't assess — no 13F filed | If 13F appears, check sector alignment |
| No unusual Q4 accumulation patterns | Q3 positions mostly maintained | **Key test** — Q4 is the "December pincer window" |
| Broad institutional accumulation in same securities | Null hypothesis supported for ORCL | If only index funds accumulated, model weakened |

---

## 4. Connection to Board of Peace / "New Gaza" / Pax Silica

### 4A. The Apollo-BoP-QXO Nexus

The 13F analysis reveals that the Board of Peace Executive Board is not merely a governance body — it has a documented financial engineering capability attached:

| BoP Executive Board Member | Financial Position | Reconstruction Relevance |
|---|---|---|
| Marc Rowan (Apollo CEO) | Runs $1T AUM, $690B+ credit; $3B to QXO; $3.5B to xAI data centers | Reported role: "design complex financial structures aimed at attracting private global capital to Gaza" (Al Jazeera, Palestine Chronicle) |
| Jared Kushner (Affinity CEO) | 100% of 13F in QXO ($623M); ~9.9% Phoenix Financial; LP base includes PIF ($2B) | "New Gaza" plan presenter; QXO controls building materials distribution |
| Yakir Gabay | Bank Leumi background; 15% Aroundtown (European real estate) | "New Gaza" plan architect; Gaza Executive Board member |

The LEAD_ANALYST_REVIEW (Section 3F, Feb 7) previously flagged Apollo/Rowan as "underexplored." The 13F Supplementary Analysis resolves this: Rowan's role is not nominal — it connects Board of Peace governance authority to Apollo's credit infrastructure, with QXO as the building materials platform.

### 4B. QXO as Reconstruction-Scale Platform

The Supplementary Analysis documents QXO's consolidation trajectory:

| Date | Acquisition | Value | Cumulative Revenue |
|---|---|---|---|
| Apr 2025 | Beacon Roofing Supply | $11B | ~$8B |
| Feb 11, 2026 | Kodiak Building Partners | $2.25B | ~$10.4B |
| Pipeline | "Very active" further targets | $10B war chest | Target: $50B |

**Product coverage:** Roofing, lumber, trusses, windows, doors, gypsum, insulation — full building envelope.
**Geography:** 26+ states; 40% of Kodiak revenue from Florida and Texas (Sun Belt).
**Named backers:** Apollo, Temasek, Affinity Partners, Sequoia Heritage.

Assessment (from Supplementary Analysis): **STRUCTURALLY PLAUSIBLE, NOT CONFIRMED.**

QXO's consolidation creates a platform *capable of* serving large-scale reconstruction. The capital chain (Gulf SWF → Affinity → QXO ← Apollo credit) connects sovereign capital to physical building materials infrastructure. No direct evidence links QXO to any specific reconstruction project. The structural capability exists; specific intent is not established.

### 4C. Pax Silica Infrastructure Layer

Apollo's credit positions connect to the Pax Silica doctrine through the digital infrastructure layer:

```
Pax Silica ("compute and the minerals that feed it")
            |
    +-----------------+------------------+
    |                 |                  |
Stream Data Centers   xAI Compute        Meta DC Expansion
(Apollo-owned, 4+ GW) ($3.5B Apollo)    ($29B Apollo co-lend)
    |                 |                  |
    Physical DC       AI training        Social infrastructure
    infrastructure    at scale           at scale
```

The connection points:
- **xAI Series E investors:** QIA (Qatar), MGX (Abu Dhabi) — both BoP signatories
- **Stream Data Centers:** Apollo owns majority stake; 4+ GW capacity = significant fraction of US data center power
- **Meta co-lending:** $29B positions Apollo at the center of social media infrastructure financing
- **Pax Silica Summit** (Dec 2025): Formalizes US tech supply chain as strategic asset; Apollo provides credit backbone

### 4D. The Board of Peace First Session — February 19 Context

The BoP first session is confirmed for February 19, 2026 (Axios). 13F filing deadline is February 17. This means:

1. Q4 2025 financial positioning data becomes available 2 days before the BoP operational session
2. Any Q4 accumulation patterns in defense/infrastructure/AI would be visible just as governance decisions are being made
3. Apollo's credit commitments ($37.5B+ pipeline) are already deployed regardless of 13F data

The timing creates a verification opportunity: cross-reference Q4 13F data with decisions announced at the Feb 19 session.

---

## 5. Updated Tier Assignments

Integrating the 13F analysis with existing Claude_Code_Analysis files:

| Entity | Previous Tier | Updated Tier | Rationale |
|---|---|---|---|
| Apollo Management Holdings | TIER 2 (13F only) | **TIER 1 — CRITICAL** | $37.5B+ credit pipeline to QXO, xAI, Meta, Stream DC; Rowan on BoP Executive Board; 13F structurally irrelevant for role assessment |
| QXO Inc | Not previously tracked | **TIER 1 — CRITICAL** | Strategic consolidation vehicle; $50B target; Apollo/Affinity/Temasek backed; full building envelope; reconstruction-scale capability |
| Affinity Partners | TIER 1 | **TIER 1+ — CONVERGENCE NODE** | Connects Gulf SWF capital → QXO → Apollo credit → building materials; 100% 13F concentration signals private portfolio dominance |
| PIF | TIER 1 | TIER 1 (unchanged) | EA 9.9% confirmed; portfolio concentrated to 6 positions |
| Mubadala | TIER 1 | TIER 1 (unchanged) | GFS 81.1% confirmed; new LMT position notable |
| Silver Lake | TIER 1 | TIER 1 (unchanged) | EA consortium; Klarna overlap with Mubadala |
| 1789 Capital | TIER 1 | TIER 1 (unchanged) | Entirely 13F-invisible; $2B AUM; private-only portfolio |
| MGX | TIER 1 | TIER 1 (unchanged) | All private; xAI Series E; TikTok USDS 15% |
| QIA | TIER 2 | TIER 2 (unchanged) | Selective filer; no Trident-sector positions visible |
| ECP | TIER 2 | TIER 2 (unchanged) | ADQ partnership is private |
| Temasek | Not tracked | **NEW — TIER 2** | QXO $1.8B co-lead with Apollo; Singapore SWF |

---

## 6. Methodology Notes

### What This Integration Does
- Cross-references Copilot 13F analysis against existing Claude_Code_Analysis files
- Identifies where the 13F data confirms, contradicts, or extends prior assessments
- Documents the Apollo credit pipeline as a structural finding
- Sets Q4 verification targets with specific baseline comparisons

### What This Integration Does Not Do
- Claim coordination or conspiracy based on documented capital flows
- Assert QXO is specifically intended for Gaza reconstruction (structurally plausible, not confirmed)
- Predict Q4 filing outcomes
- Treat absence of evidence as evidence of absence (or presence)

### Key Analytical Principle
**Absence of 13F visibility does not equal absence of activity.** The 13F visibility gap confirms the architecture operates in regulatory blind spots — through credit (not equity), private companies, non-US exchanges, and below-threshold structuring. This is a structural observation, not an accusation.

---

## 7. Files Referenced

| File | Location | Key Contribution |
|---|---|---|
| 13F_Verification_Report_Feb14_2026.md | Copilot_Opus_4.6_Analysis/13F_Analysis/ | Entity-by-entity Q3 2025 holdings; cross-entity clustering test; visibility gap documentation |
| 13F_Supplementary_Analysis_Feb14_2026.md | Copilot_Opus_4.6_Analysis/13F_Analysis/ | Apollo credit pipeline ($37.5B+); QXO consolidation; "beard" search; tier upgrades |
| 13F_Holdings_Baseline_Q3_2025.csv | Copilot_Opus_4.6_Analysis/13F_Analysis/ | Raw holdings data for all tracked entities |
| Entity_13F_Cross_Reference.csv | Copilot_Opus_4.6_Analysis/13F_Analysis/ | Entity filing status, CIK, tier assignments |
| Security_Level_Cross_Reference.csv | Copilot_Opus_4.6_Analysis/13F_Analysis/ | Security-level analysis showing cross-entity overlap |
| Pre_13F_Verification_Baseline.md | Claude_Code_Analysis/ | Original predictions; verification protocol; disconfirmation criteria |
| Privatized_Integration_Networks_Q1_2026_Synthesis.md | Claude_Code_Analysis/ | Master document; actor mapping; Part VII cross-domain table |
| Phoenix_Settlement_Portfolio_and_New_Gaza.md | Claude_Code_Analysis/ | Phoenix portfolio detail; "New Gaza" zoning analysis |
| LEAD_ANALYST_REVIEW.md | Claude_Code_Analysis/ | Running review; blind spots; verification log |

---

*Compiled: February 14, 2026*
*Methodology: Cross-reference integration of Copilot 13F analysis against Claude_Code_Analysis synthesis documents*
*Status: Pre-Q4 integration — Q4 2025 filings expected Feb 17, 2026+*
*Next action: When Q4 filings drop, run Section 3 verification targets and produce Post-13F Verification Report*
