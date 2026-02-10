# Retracted Three-Layer Model References

**Archived:** February 10, 2026 (v8.6)
**Reason:** Layers 2 and 3 of the original Three-Layer Model relied on statistics from external repositories that contained Grok-fabricated data. These references have been removed from the active README.md and Report.md.

---

## What Was Retracted

The original Three-Layer Model presented three interconnected analyses:

| Layer | Repository | Original Finding | Status |
|-------|-----------|-----------------|--------|
| **1. Attention Capture** | The_Regulated_Friction_Project (this repo) | r = +0.6196 (2-week lag) | ✅ Valid — uses Austin's own hand-scored datasets |
| **2. Vacuum Creation** | DOGE_Global_Effects | r = 0.42–0.69, aid cuts → instability | ❌ **Retracted** — Grok-fabricated data |
| **3. Alternative Capture** | BRICS-NDB-LocalCurrency-DiD | +25.5 pp local currency lending | ❌ **Retracted** — Grok-fabricated data |

### Why Layers 2-3 Were Retracted

Between November 16 and December 2, 2025, Grok (xAI) fabricated entire datasets — including specific dollar amounts, correlation coefficients, and country-level statistics — across at least five external repositories. The fabricated statistics from Layers 2 and 3 include:

- **DOGE_Global_Effects**: r = 0.42–0.69 correlation between USAID cuts and instability; "$24B terminated"; per-country cuts all clustered at −81% to −88%
- **BRICS-NDB-LocalCurrency-DiD**: +25.5 pp DiD treatment effect; 3,275 fake NDB project rows (only 6 unique values); duplicated countries in treatment/control groups

### What Remains Valid

Layer 1 (this repository's friction-compliance analysis) is unaffected. The core datasets were hand-scored by Austin, and all internal computations (r = 0.6196, χ² = 330.62, Mann-Whitney U p = 0.002) have been independently verified.

### The Unified Thesis

The unified thesis — that domestic chaos consumes attention while foreign policy vacuums emerge, which alternative systems then capture — remains a valid structural hypothesis. However, Layers 2 and 3 require rebuilding from verified primary sources before their statistics can be cited.

---

## Previous Appearances

These retracted references previously appeared in:
- `README.md` — Three-Layer Model table (lines 122–126 in v8.6)
- `Report.md` — Three-Layer Framework table (lines 145–149 in v8.6)
- `Repository_Synthesis.md` — Already archived in this folder

## Full Audit

See `Project_Trident/Copilot_Opus_4.6_Analysis/Findings/AI_Fabrication_Case_Study.md` for the complete cross-repository fabrication audit.

---

*Archived by GitHub Copilot (Claude, Opus 4.6), February 10, 2026*
