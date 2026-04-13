import pandas as pd
import numpy as np

def debug_credit():
    df_raw = pd.read_csv('.test/full_macro_data.csv', dtype={'security_id': str})
    df = df_raw.pivot(index='date', columns='security_id', values='close').ffill()
    
    # Ground Truth: AA+ Spread (AA+ Yield - CDB Yield)
    # IDs: L002959791 (AA+), L001618296 (CDB)
    gt_spread = df['L002959791'] - df['L001618296']
    
    # Proxies: Corp (H11008), Gov (H11006)
    # Provided IDs: 48919110, 47989178
    p_corp = df['48919110']
    p_gov = df['47989178']
    
    # Check returns
    r_corp = p_corp.pct_change()
    r_gov = p_gov.pct_change()
    r_gt = gt_spread.diff()
    
    # User formula: -(r_corp - r_gov)
    hf_ret = -(r_corp - r_gov)
    
    print(f"Spread Level Avg: {gt_spread.mean():.4f}")
    print(f"Spread Corrs with Proxies (Price Returns):")
    # We expect dSpread > 0 (Spread widening) -> r_corp < 0 (Price down). So negative corr.
    print(f"Corr(dSpread, r_corp): {r_gt.corr(r_corp):.4f}")
    print(f"Corr(dSpread, r_gov):  {r_gt.corr(r_gov):.4f}")
    # Widening spread -> Corp dropped MORE than Gov -> (r_corp - r_gov) < 0. So negative corr.
    print(f"Corr(dSpread, r_corp - r_gov): {r_gt.corr(r_corp - r_gov):.4f}")
    # After negation: Widening spread -> Positive signal. So positive corr.
    print(f"Corr(dSpread, -(r_corp - r_gov)): {r_gt.corr(hf_ret):.4f}")

if __name__ == "__main__":
    debug_credit()
