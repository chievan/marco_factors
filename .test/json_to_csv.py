import json
import csv
import sys

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    cols = data['object'][0]['value']
    date_col = next(c['value'] for c in cols if c['name'] == 'date')
    id_col = next(c['value'] for c in cols if c['name'] == 'security_id')
    close_col = next(c['value'] for c in cols if c['name'] == 'close')
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for d, s, c in zip(date_col, id_col, close_col):
            d_fmt = d.replace('.', '-')
            writer.writerow([d_fmt, s, c])

if __name__ == "__main__":
    if len(sys.argv) > 2:
        json_to_csv(sys.argv[1], sys.argv[2])
    else:
        # Default for backward compatibility if needed
        json_to_csv('.test/new_bond_data.json', '.test/append_data.csv')
