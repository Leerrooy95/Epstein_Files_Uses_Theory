#!/usr/bin/env python3
"""
Project Triton Statistical Verification
Analyzing ritual events vs holiday baseline correlations
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load all relevant datasets"""
    print("="*70)
    print("PROJECT TRITON STATISTICAL VERIFICATION")
    print("="*70)
    
    # Load correlation analysis
    corr_df = pd.read_csv('/mnt/user-data/uploads/Lag_Correlation_Analysis_Verified_Holidays.csv')
    
    # Load individual datasets for context
    holidays = pd.read_csv('/mnt/user-data/uploads/Holidays_2015_2025_Verified.csv')
    rituals = pd.read_csv('/mnt/user-data/uploads/ritual_events_parsed.csv')
    
    print(f"\nDataset Overview:")
    print(f"  Correlation records: {len(corr_df)}")
    print(f"  Unique holidays tracked: {len(holidays)}")
    print(f"  Unique ritual events: {len(rituals)}")
    
    return corr_df, holidays, rituals

def analyze_lag_distributions(df):
    """Analyze the distribution of ritual vs holiday lags"""
    print("\n" + "="*70)
    print("LAG DISTRIBUTION ANALYSIS")
    print("="*70)
    
    ritual_lags = df['Ritual_Lag'].abs()
    holiday_lags = df['Holiday_Lag'].abs()
    
    print("\nRitual Event Lags (absolute days):")
    print(f"  Mean: {ritual_lags.mean():.2f} days")
    print(f"  Median: {ritual_lags.median():.2f} days")
    print(f"  Std Dev: {ritual_lags.std():.2f} days")
    print(f"  Min: {ritual_lags.min()} days")
    print(f"  Max: {ritual_lags.max()} days")
    
    print("\nHoliday Lags (absolute days):")
    print(f"  Mean: {holiday_lags.mean():.2f} days")
    print(f"  Median: {holiday_lags.median():.2f} days")
    print(f"  Std Dev: {holiday_lags.std():.2f} days")
    print(f"  Min: {holiday_lags.min()} days")
    print(f"  Max: {holiday_lags.max()} days")
    
    # Temporal proximity analysis
    print("\n" + "-"*70)
    print("TEMPORAL PROXIMITY BREAKDOWN")
    print("-"*70)
    
    for window in [7, 14, 30, 60]:
        ritual_within = (ritual_lags <= window).sum()
        holiday_within = (holiday_lags <= window).sum()
        ritual_pct = (ritual_within / len(ritual_lags)) * 100
        holiday_pct = (holiday_within / len(holiday_lags)) * 100
        
        print(f"\nWithin ±{window} days:")
        print(f"  Ritual events: {ritual_within}/{len(ritual_lags)} ({ritual_pct:.1f}%)")
        print(f"  Holidays: {holiday_within}/{len(holiday_lags)} ({holiday_pct:.1f}%)")
        print(f"  Difference: {ritual_pct - holiday_pct:+.1f}%")

def statistical_significance(df):
    """Test if ritual lags are significantly different from holiday lags"""
    print("\n" + "="*70)
    print("STATISTICAL SIGNIFICANCE TESTING")
    print("="*70)
    
    ritual_lags = df['Ritual_Lag'].abs()
    holiday_lags = df['Holiday_Lag'].abs()
    
    # Mann-Whitney U test (non-parametric, no normality assumption)
    statistic, p_value = stats.mannwhitneyu(ritual_lags, holiday_lags, alternative='less')
    
    print("\nMann-Whitney U Test (Are ritual lags shorter than holiday lags?):")
    print(f"  U-statistic: {statistic:.2f}")
    print(f"  p-value: {p_value:.6f}")
    
    if p_value < 0.001:
        print(f"  Result: HIGHLY SIGNIFICANT (p < 0.001)")
        print(f"  Interpretation: Ritual lags are significantly shorter than holiday lags")
    elif p_value < 0.05:
        print(f"  Result: SIGNIFICANT (p < 0.05)")
        print(f"  Interpretation: Ritual lags are significantly shorter than holiday lags")
    else:
        print(f"  Result: NOT SIGNIFICANT (p ≥ 0.05)")
        print(f"  Interpretation: No significant difference detected")
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt((ritual_lags.std()**2 + holiday_lags.std()**2) / 2)
    cohens_d = (ritual_lags.mean() - holiday_lags.mean()) / pooled_std
    
    print(f"\nEffect Size (Cohen's d): {cohens_d:.3f}")
    if abs(cohens_d) < 0.2:
        effect = "negligible"
    elif abs(cohens_d) < 0.5:
        effect = "small"
    elif abs(cohens_d) < 0.8:
        effect = "medium"
    else:
        effect = "large"
    print(f"  Interpretation: {effect.upper()} effect size")

def analyze_by_category(df):
    """Break down correlations by category"""
    print("\n" + "="*70)
    print("CATEGORY-SPECIFIC ANALYSIS")
    print("="*70)
    
    categories = df['Category'].unique()
    
    for cat in categories:
        cat_df = df[df['Category'] == cat]
        ritual_lags = cat_df['Ritual_Lag'].abs()
        holiday_lags = cat_df['Holiday_Lag'].abs()
        
        print(f"\n{cat}:")
        print(f"  Events: {len(cat_df)}")
        print(f"  Ritual lag (mean): {ritual_lags.mean():.1f} days")
        print(f"  Holiday lag (mean): {holiday_lags.mean():.1f} days")
        print(f"  Advantage: {holiday_lags.mean() - ritual_lags.mean():+.1f} days")

def analyze_december_cluster(df):
    """Specific analysis of December 2025 cluster"""
    print("\n" + "="*70)
    print("DECEMBER 2025 CLUSTER ANALYSIS")
    print("="*70)
    
    # Filter to December 2025 actions
    df['Action_Date'] = pd.to_datetime(df['Action_Date'])
    december = df[
        (df['Action_Date'] >= '2025-12-01') & 
        (df['Action_Date'] <= '2025-12-31')
    ]
    
    if len(december) > 0:
        print(f"\nDecember 2025 Events: {len(december)}")
        
        ritual_lags = december['Ritual_Lag'].abs()
        holiday_lags = december['Holiday_Lag'].abs()
        
        print(f"\nTemporal Proximity:")
        print(f"  Ritual lag (mean): {ritual_lags.mean():.1f} days")
        print(f"  Holiday lag (mean): {holiday_lags.mean():.1f} days")
        
        print(f"\nEvents within ±7 days:")
        print(f"  Ritual: {(ritual_lags <= 7).sum()} events ({(ritual_lags <= 7).sum()/len(ritual_lags)*100:.1f}%)")
        print(f"  Holiday: {(holiday_lags <= 7).sum()} events ({(holiday_lags <= 7).sum()/len(holiday_lags)*100:.1f}%)")
        
        print(f"\nDecember 2025 Actions:")
        for _, row in december.sort_values('Action_Date').iterrows():
            print(f"  {row['Action_Date'].strftime('%Y-%m-%d')}: {row['Action_Title'][:60]}")
            print(f"    → Ritual lag: {abs(row['Ritual_Lag'])} days | Holiday lag: {abs(row['Holiday_Lag'])} days")
    else:
        print("\nNo December 2025 events found in dataset")

def correlation_coefficient_analysis(df):
    """Calculate actual Pearson correlations"""
    print("\n" + "="*70)
    print("CORRELATION COEFFICIENT ANALYSIS")
    print("="*70)
    
    # For correlation, we need a binary/continuous variable
    # Let's use "proximity score" - inverse of absolute lag
    
    df['Ritual_Proximity'] = 1 / (df['Ritual_Lag'].abs() + 1)
    df['Holiday_Proximity'] = 1 / (df['Holiday_Lag'].abs() + 1)
    
    # Create a simple score: events within 14 days = 1, else = 0
    df['Ritual_14day'] = (df['Ritual_Lag'].abs() <= 14).astype(int)
    df['Holiday_14day'] = (df['Holiday_Lag'].abs() <= 14).astype(int)
    
    print("\nProximity Correlations:")
    print(f"  Note: Higher values = events closer in time")
    print(f"\nRitual Proximity Score:")
    print(f"  Mean: {df['Ritual_Proximity'].mean():.4f}")
    print(f"  Within 14 days: {df['Ritual_14day'].mean()*100:.1f}%")
    
    print(f"\nHoliday Proximity Score:")
    print(f"  Mean: {df['Holiday_Proximity'].mean():.4f}")
    print(f"  Within 14 days: {df['Holiday_14day'].mean()*100:.1f}%")
    
    # Ratio
    ratio = df['Ritual_Proximity'].mean() / df['Holiday_Proximity'].mean()
    print(f"\nRitual/Holiday Proximity Ratio: {ratio:.2f}x")
    print(f"  Interpretation: Ritual events are {ratio:.1f}x closer temporally to actions than holidays")

def main():
    # Load data
    corr_df, holidays, rituals = load_data()
    
    # Run analyses
    analyze_lag_distributions(corr_df)
    statistical_significance(corr_df)
    correlation_coefficient_analysis(corr_df)
    analyze_by_category(corr_df)
    analyze_december_cluster(corr_df)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    ritual_lags = corr_df['Ritual_Lag'].abs()
    holiday_lags = corr_df['Holiday_Lag'].abs()
    
    print(f"\nKey Finding:")
    print(f"  Ritual events are {holiday_lags.mean() - ritual_lags.mean():.1f} days closer")
    print(f"  on average to policy/infrastructure actions than holidays")
    print(f"\nStatistical Strength:")
    
    # Recalculate p-value for summary
    _, p_value = stats.mannwhitneyu(ritual_lags, holiday_lags, alternative='less')
    if p_value < 0.001:
        print(f"  p < 0.001 (HIGHLY SIGNIFICANT)")
    else:
        print(f"  p = {p_value:.4f}")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    main()
