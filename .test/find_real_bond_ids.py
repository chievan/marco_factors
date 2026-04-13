import pandas as pd
import numpy as np

def find_ids():
    df_raw = pd.read_csv('.test/full_macro_data.csv', dtype={'security_id': str})
    df = df_raw.pivot(index='date', columns='security_id', values='close').ffill()
    
    # Ground Truth: AA+ Spread
    gt_spread = df['L002959791'] - df['L001618296']
    r_gt = gt_spread.diff()
    
    # Search candidates (IDs starting with 4)
    candidates = [c for c in df.columns if c.startswith('4')]
    
    results = []
    for c in candidates:
        r = df[c].pct_change()
        corr = r_gt.corr(r)
        std = r.std()
        results.append({'id': c, 'corr': corr, 'std': std})
    
    res_df = pd.DataFrame(results).sort_values('corr')
    print("Correlations with Spread Widening (Targeting Negative):")
    print(res_df.head(20))

if __name__ == "__main__":
    find_ids()
