import csv
import os

# Helper functions to read CSV into dicts
def read_csv_to_dict(filename, key_col):
    result = {}
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row[key_col]
            result[key] = {k: v for k, v in row.items() if k != key_col}
    return result

def read_csv_to_list(filename):
    result = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append(row)
    return result

# Join implementations
def inner_join(a_rows, b_dict, a_key, b_key, a_val, b_val):
    joined = []
    for row in a_rows:
        id_ = row[a_key]
        if id_ in b_dict:
            joined.append((id_, int(row[a_val]), int(b_dict[id_][b_val])))
    return joined

def left_join(a_rows, b_dict, a_key, b_key, a_val, b_val):
    joined = []
    for row in a_rows:
        id_ = row[a_key]
        price = int(row[a_val])
        qty = int(b_dict[id_][b_val]) if id_ in b_dict else None
        joined.append((id_, price, qty))
    return joined

# Unit tests
def test_joins():
    # Create sample CSV files
    a_csv = 'A.csv'
    b_csv = 'B.csv'
    with open(a_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'price'])
        writer.writerow(['A', '10'])
        writer.writerow(['B', '20'])
    with open(b_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'qty'])
        writer.writerow(['A', '2'])
        writer.writerow(['C', '5'])

    # Read data
    a_rows = read_csv_to_list(a_csv)
    b_dict = read_csv_to_dict(b_csv, 'id')

    # Perform joins
    inner = inner_join(a_rows, b_dict, 'id', 'id', 'price', 'qty')
    left = left_join(a_rows, b_dict, 'id', 'id', 'price', 'qty')

    # Check results
    assert inner == [('A', 10, 2)], f"Inner join failed: {inner}"
    assert left == [('A', 10, 2), ('B', 20, None)], f"Left join failed: {left}"

    print("inner=", inner)
    print("left=", left)

    # Cleanup
    os.remove(a_csv)
    os.remove(b_csv)

if __name__ == "__main__":
    test_joins()