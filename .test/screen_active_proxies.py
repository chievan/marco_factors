import pandas as pd
import numpy as np

def find_active_proxies():
    df_raw = pd.read_csv('.test/full_macro_data.csv', dtype={'security_id': str})
    df = df_raw.pivot(index='date', columns='security_id', values='close').ffill()
    active_ids = [c for c in df.columns if c.startswith('4') and df[c].last_valid_index() >= pd.to_datetime('2026-04-01')]
    
    # Ground Truth: Spread
    gt_spread = df['L002959791'] - df['L001618296']
    r_gt = gt_spread.diff()
    r_rates = df['48488928'].pct_change()
    
    results = []
    for c in active_ids:
        r = df[c].pct_change()
        results.append({
            'id': c,
            'corr_rates': r.corr(r_rates),
            'corr_spread': r.corr(r_gt),
            'vol': r.std()
        })
    
    res_df = pd.DataFrame(results).sort_values('vol')
    print("Proxies with data in 2026:")
    print(res_df)

if __name__ == "__main__":
    find_active_proxies()
