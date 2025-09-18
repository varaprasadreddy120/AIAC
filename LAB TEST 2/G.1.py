import csv

def sum_valid_values(csv_file_path):
    total = 0
    skipped = 0
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                value = int(row['value'])
                
                total += value
            except (ValueError, KeyError):
                skipped += 1
    print(total)
    print(f"Skipped rows: {skipped}")

# --- Test code ---
if __name__ == "__main__":
    # Create a sample CSV for testing
    test_csv = 'test.csv'
    with open(test_csv, 'w', newline='') as f:
        f.write('id,value\n1,10\n2,NA\n3,7\n')
    sum_valid_values(test_csv)