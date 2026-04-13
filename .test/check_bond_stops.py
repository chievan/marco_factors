import pandas as pd

def check_stop_dates():
    df_raw = pd.read_csv('.test/full_macro_data.csv', dtype={'security_id': str})
    df = df_raw.pivot(index='date', columns='security_id', values='close')
    
    bond_candidates = ['44900702', '48129734', '47989178', '40525479', '49862409', '48919110', '48488928']
    
    print("ID              Last_Date    Last_Val")
    for c in bond_candidates:
        if c in df.columns:
            last_idx = df[c].last_valid_index()
            last_val = df[c][last_idx]
            print(f"{c:<15} {last_idx} {last_val:>10.2f}")

if __name__ == "__main__":
    check_stop_dates()
