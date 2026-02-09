#!/usr/bin/env python3
"""
Shared data-loading utilities for the original pre-2026 datasets.

These are the EXACT datasets Austin used for the original correlations
(v3.1–v5.5, December 22–25, 2025).  New_Data_2026/ is explicitly excluded.

Original datasets and their roles:
  FRICTION (trigger) sources:
    - ritual_events_parsed.csv          — 51 ritual trigger events
    - temporal_correlations_analyzed.csv — 338 ritual-anchor pairings with lag_days
    - Holidays_2015_2025_Verified.csv   — 59 verified holiday dates
    - MASTER_reflexive_control_v2.csv   — 149 reflexive control events (w/ Theory_Label)
    - thermostat_control_data.csv       — 150 thermostat events (w/ Theory_Label)

  COMPLIANCE (response/anchor) sources:
    - anchor_events_parsed.csv          — 70 institutional anchor events
    - project_trident_final_dossier.csv — 118 dossier entries (Authority/Finance/Hardware/Geopolitics)
    - Lag_Correlation_Analysis_Verified_Holidays.csv — 533 policy actions with lag measurements
    - Expanded_Policy_Anchors.csv       — 11 policy anchors
    - aid_timeline_clean.csv            — 190 US aid timeline entries
    - policy_cleaned.csv                — 60 policy events
    - tech_filled_dates.csv             — 357 technology events

  MIXED / PERIODICITY sources (Silicon Sovereignty — used for chi-square):
    - Coalition_Narrative_Map_2015-2025.csv      — 456 narrative events
    - VOCA_funding_timeline_clean.csv            — 667 funding events
    - Regulatory_Map_Data_CLEANED.csv            — 76 regulatory events
    - REFINED_supercomputer_geopolitics (1).csv  — 906 hardware events
    - Fund_Flow_Ritual_Coordination_2025.csv     — 97 fund flow events

  INDEX-SCORED source (Part 1):
    - master_reflexive_correlation_data.csv — 30 weeks pre-scored friction/compliance
"""

import os
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore', category=FutureWarning)

_script_dir = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(_script_dir, '..', 'Datasets')
REPO_ROOT = os.path.join(_script_dir, '..', '..', '..')


# ── Friction (trigger) event types ───────────────────────────────────────────
# These map to Austin's original "friction" concept: events that create
# public noise / attention / disruption.

FRICTION_RITUAL_TYPES = {
    'Temple Mount Foundation Stone Laying', 'Sanhedrin Convocation',
    'Papal Extraordinary Consistory', 'Evangelical Temple Delegation',
    'Grand Mufti Al-Aqsa Declaration', 'Red Heifer Ceremony',
}

# Vectors in the dossier that represent friction
FRICTION_VECTORS = {
    'AUTHORITY (Political)', 'HARDWARE (Ritual)',
}

# ── Compliance (response) event types ────────────────────────────────────────
# These map to Austin's original "compliance" concept: institutional responses
# like tech deals, policy shifts, financial moves.

COMPLIANCE_ANCHOR_CATEGORIES = {
    'Oracle_Tech', 'Oracle_Infrastructure', 'Palantir_Defense',
    'US_AI_Policy', 'Israel_Tech_Funding', 'Israel_Defense',
    'Crypto_Event',
}

COMPLIANCE_VECTORS = {
    'FINANCE (Black Budget)', 'GEOPOLITICS (The Prize)',
}

COMPLIANCE_LAG_CATEGORIES = {
    'Expanded_Policy_Anchor', 'AI_Policy', 'Aid_Tech', 'Tech_Events',
}

# Date column candidates across all original datasets
DATE_COLS = [
    'date_parsed_v2', 'date_parsed', 'date_found', 'Date', 'date',
    'Event_Date', 'event_date', 'Published_Date', 'Action_Date',
    'ritual_date', 'anchor_date', 'aid_date', 'policy_date',
]


def _find_date_col(df):
    """Find the best date column in a DataFrame."""
    for col in DATE_COLS:
        if col in df.columns:
            return col
    return None


def load_friction_events():
    """Load all friction (trigger) events from original datasets.
    
    Returns a DataFrame with columns: date, source, detail
    """
    rows = []

    # 1. Ritual events parsed (51 events)
    path = os.path.join(DATASETS_DIR, 'ritual_events_parsed.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, r in df.iterrows():
            d = pd.to_datetime(r.get('date_parsed_v2') or r.get('date_found'),
                               errors='coerce')
            if pd.notna(d):
                rows.append({'date': d, 'source': 'ritual_events',
                             'detail': r.get('ritual_type', '')})

    # 2. Holidays (59 verified dates — used as friction timing markers)
    path = os.path.join(DATASETS_DIR, 'Holidays_2015_2025_Verified.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, r in df.iterrows():
            d = pd.to_datetime(r.get('date'), errors='coerce')
            if pd.notna(d):
                rows.append({'date': d, 'source': 'holidays',
                             'detail': r.get('ritual_type', '')})

    # 3. Dossier friction vectors (AUTHORITY + HARDWARE)
    path = os.path.join(DATASETS_DIR, 'project_trident_final_dossier.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, r in df.iterrows():
            vec = str(r.get('Vector', ''))
            if vec in FRICTION_VECTORS:
                d = pd.to_datetime(r.get('Date'), errors='coerce')
                if pd.notna(d):
                    rows.append({'date': d, 'source': 'dossier_friction',
                                 'detail': vec})

    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=['date', 'source', 'detail'])


def load_compliance_events():
    """Load all compliance (response/anchor) events from original datasets.
    
    Returns a DataFrame with columns: date, source, detail
    """
    rows = []

    # 1. Anchor events parsed (70 events)
    path = os.path.join(DATASETS_DIR, 'anchor_events_parsed.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, r in df.iterrows():
            d = pd.to_datetime(r.get('date_parsed_v2') or r.get('date_found'),
                               errors='coerce')
            if pd.notna(d):
                rows.append({'date': d, 'source': 'anchor_events',
                             'detail': r.get('anchor_category', '')})

    # 2. Dossier compliance vectors (FINANCE + GEOPOLITICS)
    path = os.path.join(DATASETS_DIR, 'project_trident_final_dossier.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, r in df.iterrows():
            vec = str(r.get('Vector', ''))
            if vec in COMPLIANCE_VECTORS:
                d = pd.to_datetime(r.get('Date'), errors='coerce')
                if pd.notna(d):
                    rows.append({'date': d, 'source': 'dossier_compliance',
                                 'detail': vec})

    # 3. Lag correlation actions (533 policy actions — these ARE the compliance events)
    path = os.path.join(DATASETS_DIR, 'Lag_Correlation_Analysis_Verified_Holidays.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, r in df.iterrows():
            d = pd.to_datetime(r.get('Action_Date'), errors='coerce')
            if pd.notna(d):
                rows.append({'date': d, 'source': 'lag_policy_actions',
                             'detail': r.get('Category', '')})

    # 4. Expanded policy anchors (11 events)
    path = os.path.join(DATASETS_DIR, 'Expanded_Policy_Anchors.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, r in df.iterrows():
            d = pd.to_datetime(r.get('policy_date'), errors='coerce')
            if pd.notna(d):
                rows.append({'date': d, 'source': 'expanded_policy',
                             'detail': r.get('policy_event', '')})

    # 5. Policy cleaned (60 events)
    path = os.path.join(DATASETS_DIR, 'policy_cleaned.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        date_col = _find_date_col(df)
        if date_col:
            for _, r in df.iterrows():
                d = pd.to_datetime(r.get(date_col), errors='coerce')
                if pd.notna(d):
                    rows.append({'date': d, 'source': 'policy_cleaned',
                                 'detail': ''})

    # 6. Tech filled dates (357 events)
    path = os.path.join(DATASETS_DIR, 'tech_filled_dates.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        date_col = _find_date_col(df)
        if date_col:
            for _, r in df.iterrows():
                d = pd.to_datetime(r.get(date_col), errors='coerce')
                if pd.notna(d):
                    rows.append({'date': d, 'source': 'tech_filled',
                                 'detail': ''})

    # 7. Aid timeline (190 events)
    path = os.path.join(DATASETS_DIR, 'aid_timeline_clean.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, r in df.iterrows():
            d = pd.to_datetime(r.get('aid_date'), errors='coerce')
            if pd.notna(d):
                # Strip timezone info for consistency
                if hasattr(d, 'tz') and d.tz is not None:
                    d = d.tz_localize(None)
                rows.append({'date': d, 'source': 'aid_timeline',
                             'detail': r.get('Category', '')})

    result = pd.DataFrame(rows) if rows else pd.DataFrame(columns=['date', 'source', 'detail'])
    # Ensure all dates are tz-naive for consistency
    if len(result) > 0:
        result['date'] = result['date'].apply(
            lambda d: d.tz_localize(None) if hasattr(d, 'tzinfo') and d.tzinfo is not None else d
        )
    return result


def load_all_dated_events():
    """Load ALL dated events from Silicon Sovereignty datasets (for periodicity/chi-square).
    
    These are the datasets from the v5.5 cross-validation analysis.
    Returns DataFrame with columns: date, source
    """
    files = {
        'Coalition_Narrative': ('Coalition_Narrative_Map_2015-2025.csv', 'Published_Date'),
        'VOCA_Funding': ('VOCA_funding_timeline_clean.csv', 'Event_Date'),
        'Regulatory_Map': ('Regulatory_Map_Data_CLEANED.csv', 'Event_Date'),
        'Supercomputer_Geopolitics': ('REFINED_supercomputer_geopolitics (1).csv', 'Event_Date'),
    }

    rows = []
    for name, (filename, date_col) in files.items():
        path = os.path.join(DATASETS_DIR, filename)
        if not os.path.exists(path):
            print(f"  ⚠ skipping {filename} (not found)")
            continue
        df = pd.read_csv(path)
        if date_col not in df.columns:
            print(f"  ⚠ skipping {filename} (no {date_col} column)")
            continue
        dates = pd.to_datetime(df[date_col], errors='coerce').dropna()
        for d in dates:
            rows.append({'date': d, 'source': name})

    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=['date', 'source'])


def load_temporal_correlations():
    """Load the pre-computed temporal correlation pairings (338 records).
    
    These directly encode ritual→anchor lag relationships from Austin's
    original Project Trident analysis.
    """
    path = os.path.join(DATASETS_DIR, 'temporal_correlations_analyzed.csv')
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    df['ritual_date'] = pd.to_datetime(df['ritual_date'], errors='coerce')
    df['anchor_date'] = pd.to_datetime(df['anchor_date'], errors='coerce')
    return df


def load_lag_correlation():
    """Load the verified lag correlation analysis (533 records).
    
    Each row is a policy action with measured distance to nearest ritual
    and nearest holiday.
    """
    path = os.path.join(DATASETS_DIR, 'Lag_Correlation_Analysis_Verified_Holidays.csv')
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def build_weekly_counts(friction_df, compliance_df, start=None, end=None):
    """Build weekly friction/compliance counts from event DataFrames.
    
    Args:
        friction_df: DataFrame with 'date' column
        compliance_df: DataFrame with 'date' column
        start: start date string (optional, auto-detected from data)
        end: end date string (optional, auto-detected from data)
    
    Returns:
        DataFrame with columns 'friction', 'compliance' indexed by weekly Period
    """
    # Filter to reasonable date range (1990-2026)
    min_date = pd.Timestamp('1990-01-01')
    max_date = pd.Timestamp('2026-12-31')
    
    f = friction_df[friction_df['date'].between(min_date, max_date)].copy()
    c = compliance_df[compliance_df['date'].between(min_date, max_date)].copy()

    if start is None:
        all_dates = pd.concat([f[['date']], c[['date']]])
        start = all_dates['date'].min()
    if end is None:
        all_dates = pd.concat([f[['date']], c[['date']]])
        end = all_dates['date'].max()

    f['week'] = f['date'].dt.to_period('W')
    c['week'] = c['date'].dt.to_period('W')

    f_counts = f.groupby('week').size().rename('friction')
    c_counts = c.groupby('week').size().rename('compliance')

    # Create full index
    sp = pd.Period(start, 'W')
    ep = pd.Period(end, 'W')
    full_idx = pd.period_range(sp, ep, freq='W')
    
    wk = pd.DataFrame(index=full_idx)
    wk['friction'] = f_counts.reindex(full_idx, fill_value=0)
    wk['compliance'] = c_counts.reindex(full_idx, fill_value=0)

    return wk
