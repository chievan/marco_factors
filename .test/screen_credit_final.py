import pandas as pd

def find_credit_active():
    df_raw = pd.read_csv('.test/full_macro_data.csv', dtype={'security_id': str})
    df = df_raw.pivot(index='date', columns='security_id', values='close').ffill()
    
    # 10Y Gov Reference
    r_rates = df['48488928'].pct_change()
    
    # Active IDs to test
    candidates = ['45645208', '45709958', '41021909', '48714340', '45128117', '43944213']
    
    print("ID              Corr_Rates    Std_Dev    Last_Val")
    for c in candidates:
        if c in df.columns:
            r = df[c].pct_change()
            corr = r.corr(r_rates)
            std = r.std()
            val = df[c].iloc[-1]
            print(f"{c:<15} {corr:>10.4f} {std:>10.6f} {val:>10.2f}")

if __name__ == "__main__":
    find_credit_active()
