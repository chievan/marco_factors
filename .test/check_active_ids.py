import pandas as pd

def check_active():
    df_raw = pd.read_csv('.test/full_macro_data.csv', dtype={'security_id': str})
    df = df_raw.pivot(index='date', columns='security_id', values='close')
    latest = df.apply(lambda x: x.last_valid_index())
    active = latest[latest >= '2026-04-01']
    
    print("=== Active IDs in 2026 ===")
    for id_val, last_date in active.items():
        # Get a sample value to guess the type
        val = df[id_val].dropna().iloc[-1]
        print(f"ID: {id_val:<15} Last Date: {last_date} Last Value: {val:>10.2f}")

if __name__ == "__main__":
    check_active()
