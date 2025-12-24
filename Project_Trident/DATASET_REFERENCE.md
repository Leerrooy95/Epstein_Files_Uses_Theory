# Project Trident: Data Reference Guide

This document defines the schema and purpose for the datasets contained within the Project Trident folder.

### 1. `project_trident_final_dossier.csv`
The master ledger of 118 records containing the core vectors (Authority, Hardware, Finance) and their respective threat levels.

### 2. `anchor_events_parsed.csv`
A collection of 70+ institutional milestones, including the Oracle-TikTok $14B deal, US AI policy shifts, and global infrastructure expansions.

### 3. `ritual_events_parsed.csv`
A ledger of 51 religious and ritual signals used as the primary "Triggers" for temporal correlation analysis.

### 4. `temporal_correlations_analyzed.csv`
The output of the correlation engine. Maps the `lag_days` between Ritual and Anchor events. 
* **Average Lag:** 6.6 days.
* **Peak Lag Accuracy:** 14 days (r = 0.6196).

### 5. `PROJECT_TRIDENT_CASE_STUDY.md`
The formal narrative report synthesized from the above data points.

**data_complete (True/False): Flags row integrity. True = fully parsed/complete (exact date, full snippet, verified fields). False = partial/incomplete (e.g., vague date like "2 months ago", missing elements, or needs manual review). Does NOT indicate event validity—all rows are sourced signals for correlation testing.**
