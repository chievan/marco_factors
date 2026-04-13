import pandas as pd

def find_pos_corrs():
    df_raw = pd.read_csv('.test/full_macro_data.csv', dtype={'security_id': str})
    df = df_raw.pivot(index='date', columns='security_id', values='close').ffill()
    
    ref = df['48488928'].pct_change()
    
    res = []
    for c in df.columns:
        if c == '48488928': continue
        r = df[c].pct_change()
        if r.std() > 0:
            res.append({'id': c, 'corr': r.corr(ref), 'last_val': df[c].iloc[-1]})
    
    df_res = pd.DataFrame(res).sort_values('corr', ascending=False)
    print("IDs Positively Correlated with 10Y Price (Bond-like):")
    print(df_res.head(20))

if __name__ == "__main__":
    find_pos_corrs()
