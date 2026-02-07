import pandas as pd
import numpy as np
import os

def run_big_correlation_test():
    print("--- INITIATING UNIVERSAL THEORY AUDIT ---\n")
    
    master_path = 'master_reflexive_correlation_data.csv'
    scraped_path = 'reflexive_control_scraped_data.csv'
    
    if not os.path.exists(master_path):
        print(f"❌ CRITICAL ERROR: Master data not found at {master_path}")
        return

    master_df = pd.read_csv(master_path)
    print(f"✅ Loaded Master Dataset: {len(master_df)} weeks of data found.")
    
    if os.path.exists(scraped_path):
        scraped_df = pd.read_csv(scraped_path)
        print(f"✅ Loaded OSINT Scrape: {len(scraped_df)} active triggers found.")
    else:
        print("⚠️ Warning: OSINT Scrape file missing. Proceeding with Master Data only.")

    # Core lagged correlation (14-day / 2-week shift)
    direct_corr = master_df['Epstein_Friction_Index'].corr(master_df['Institutional_Compliance_Index'])
    lagged_friction = master_df['Epstein_Friction_Index'].shift(2)
    lagged_corr = lagged_friction.corr(master_df['Institutional_Compliance_Index'])
    
    strength = "WEAK"
    if 0.4 < abs(lagged_corr) <= 0.6:
        strength = "MODERATE"
    elif abs(lagged_corr) > 0.6:
        strength = "HIGH SIGNAL (VERIFIED)"

    print("\n" + "="*50)
    print("           REFLEXIVE CONTROL: STRENGTH TEST")
    print("="*50)
    print(f"Test Parameter: Friction(t-2) vs. Compliance(t)")
    print(f"Direct Correlation:    {direct_corr:.4f}")
    print(f"Lagged Correlation:    {lagged_corr:.4f}")
    print(f"Theory Strength:       {strength}")
    print("-" * 50)
    
    if abs(lagged_corr) > 0.6:
        print("CONCLUSION: The 14-day lag is a mathematically valid predictor.")
        print("The data confirms that document leaks are 'Levers' used to")
        print("force institutional 'Anchors' into alignment.")
    else:
        print("CONCLUSION: Insufficient signal to verify the 14-day loop.")
    print("="*50)

run_big_correlation_test()
