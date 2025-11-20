#!/usr/bin/env python3
"""
TASK1.PY - Bank Customer CSV Data Cleaning Tool

AI-assisted utilities to clean bank customer CSV records:
- Clean missing values (drop rows with missing required fields, fill optional fields)
- Remove duplicates (intelligent deduplication based on email, phone, or custom fields)
- Standardize phone numbers (convert to consistent E.164-like format)

Requirements:
- Python 3.7+
- pandas (install with: pip install pandas)

Usage:
    # Run demonstration (generates sample CSV and processes it):
    python TASK1.PY
    
    # Run unit tests:
    python TASK1.PY --test
    
    # Use as a module:
    from TASK1 import process_csv
    process_csv('input.csv', 'output.csv', 
                required_fields=['email', 'phone'],
                dedupe_subset=['email'])

Features:
- Handles various phone number formats (US, international)
- Email normalization for duplicate detection
- Configurable required fields and default values
- Comprehensive unit tests included
- Generates sample CSV files for testing

Author: AI-Assisted Development
Date: 2024
"""

from typing import List, Dict, Optional
import re
import pandas as pd
import unittest


# -----------------------
# Core processing helpers
# -----------------------

def load_csv(path: str) -> pd.DataFrame:
    """
    Load CSV into DataFrame, treating all values as strings and trimming whitespace.
    """
    df = pd.read_csv(path, dtype=str, keep_default_na=False)  # keep_default_na=False so empty cells are empty strings
    # Normalize types: convert NaNs/None to empty strings, trim whitespace
    df = df.fillna('').astype(str)
    for c in df.columns:
        df[c] = df[c].str.strip()
    return df


def clean_missing_values(df: pd.DataFrame,
                         required_fields: Optional[List[str]] = None,
                         fill_values: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Clean missing values:
    - Trim whitespace (already idempotent)
    - Drop rows missing any required_fields (if provided)
    - Fill optional fields using fill_values mapping

    Returns a new DataFrame (does not modify input).
    """
    df = df.copy()
    # ensure string-typed and trimmed
    df = df.fillna('').astype(str)
    for c in df.columns:
        df[c] = df[c].str.strip()

    if required_fields:
        # Consider empty string as missing
        missing_mask = pd.Series(False, index=df.index)
        for f in required_fields:
            if f in df.columns:
                missing_mask |= (df[f] == '')  # mark rows missing this required field
            else:
                # If the required field is entirely absent, treat all rows as missing
                missing_mask |= True
        df = df.loc[~missing_mask].reset_index(drop=True)

    if fill_values:
        for k, v in fill_values.items():
            if k in df.columns:
                df[k] = df[k].replace({'': v})
            else:
                # If column missing, create it with default value
                df[k] = v

    return df


def normalize_email(email: str) -> str:
    """
    Simple email normalization: lower-case and trim.
    (Does not validate RFC; intended for de-duplication use.)
    """
    return (email or '').strip().lower()


def remove_duplicates(df: pd.DataFrame,
                      subset: Optional[List[str]] = None,
                      keep: str = 'first') -> pd.DataFrame:
    """
    Remove duplicate rows.

    - subset: list of columns to consider for duplicates. If None, use ['customer_id', 'email', 'phone'] where present.
    - keep: 'first' or 'last'

    Returns a new DataFrame (does not modify input).
    """
    df = df.copy().reset_index(drop=True)

    if subset is None:
        # pick sensible defaults among available columns
        preferred = ['customer_id', 'email', 'phone']
        subset = [c for c in preferred if c in df.columns]
        if not subset:
            # fallback to all columns
            subset = list(df.columns)

    # Normalize columns used in subset to improve detection
    if 'email' in subset and 'email' in df.columns:
        df['__email_norm__'] = df['email'].astype(str).apply(normalize_email)
        subset = ['__email_norm__' if c == 'email' else c for c in subset]

    # Normalize phone: remove formatting but keep digits only for dedupe
    if 'phone' in subset and 'phone' in df.columns:
        df['__phone_digits__'] = df['phone'].astype(str).apply(lambda s: re.sub(r'\D', '', s or ''))
        subset = ['__phone_digits__' if c == 'phone' else c for c in subset]

    df = df.drop_duplicates(subset=subset, keep=keep).reset_index(drop=True)

    # Clean up helper columns
    df = df.drop(columns=[c for c in ('__email_norm__', '__phone_digits__') if c in df.columns])
    return df


def standardize_phone_number(phone: str, default_country: str = 'US') -> str:
    """
    Standardize a phone number string into a readable E.164-like format:
    +<country_code>-<area>-<prefix>-<line>

    Rules:
    - Strip all non-digit characters.
    - If digits length == 10 -> assume default_country is a country with 10-digit national significant number (e.g., US),
      and prepend country code '1' for US. Format: +1-AAA-BBB-CCCC
    - If digits length == 11 and starts with '1' -> treat as US number.
    - If digits length > 10 -> treat leading digits as country code, last 10 digits as subscriber (formatted).
    - If digits shorter than 7 -> return digits as-is (insufficient).
    - Empty or non-numeric input returns empty string.

    Note: This is a pragmatic formatter and not a substitute for the 'phonenumbers' library for full international support.
    """
    if not phone:
        return ''

    digits = re.sub(r'\D', '', str(phone))
    if not digits:
        return ''

    # US-specific handling
    if (len(digits) == 10) or (len(digits) == 11 and digits.startswith('1')):
        if len(digits) == 11:
            digits = digits[1:]  # strip leading 1
        country = '1'
        area, prefix, line = digits[:3], digits[3:6], digits[6:10]
        return f'+{country}-{area}-{prefix}-{line}'

    # Generic: treat last 10 digits as subscriber and rest as country code
    if len(digits) > 10:
        country = digits[:-10]
        subscriber = digits[-10:]
        area, prefix, line = subscriber[:3], subscriber[3:6], subscriber[6:10]
        return f'+{country}-{area}-{prefix}-{line}'

    # Short numbers (e.g., extensions) — return as-is
    return digits


def standardize_phone_numbers(df: pd.DataFrame, phone_field: str = 'phone', default_country: str = 'US') -> pd.DataFrame:
    """
    Apply standardize_phone_number to the DataFrame's phone_field.
    Returns a new DataFrame (does not modify input).
    """
    df = df.copy()
    if phone_field not in df.columns:
        df[phone_field] = ''
    df[phone_field] = df[phone_field].astype(str).apply(lambda s: standardize_phone_number(s, default_country=default_country))
    return df


def process_dataframe(df: pd.DataFrame,
                      required_fields: Optional[List[str]] = None,
                      fill_values: Optional[Dict[str, str]] = None,
                      dedupe_subset: Optional[List[str]] = None,
                      phone_field: str = 'phone',
                      default_country: str = 'US') -> pd.DataFrame:
    """
    Full pipeline: clean missing, dedupe, standardize phones.
    """
    df = clean_missing_values(df, required_fields=required_fields, fill_values=fill_values)
    df = remove_duplicates(df, subset=dedupe_subset)
    df = standardize_phone_numbers(df, phone_field=phone_field, default_country=default_country)
    return df


def process_csv(in_path: str, out_path: str,
                required_fields: Optional[List[str]] = None,
                fill_values: Optional[Dict[str, str]] = None,
                dedupe_subset: Optional[List[str]] = None,
                phone_field: str = 'phone',
                default_country: str = 'US') -> None:
    """
    Read CSV, process, and write output CSV. Overwrites out_path.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file (will be created/overwritten)
        required_fields: List of column names that must not be empty (rows with empty values will be dropped)
        fill_values: Dictionary mapping column names to default values for empty cells
        dedupe_subset: List of columns to use for duplicate detection (None = auto-detect)
        phone_field: Name of the phone number column to standardize
        default_country: Default country code for phone number standardization (default: 'US')
    """
    df = load_csv(in_path)
    out = process_dataframe(df,
                            required_fields=required_fields,
                            fill_values=fill_values,
                            dedupe_subset=dedupe_subset,
                            phone_field=phone_field,
                            default_country=default_country)
    out.to_csv(out_path, index=False)
    print(f"[OK] Processed CSV saved to: {out_path}")
    print(f"  Original rows: {len(df)}, Cleaned rows: {len(out)}")


def generate_sample_csv(output_path: str = 'customers_raw.csv') -> None:
    """
    Generate a sample CSV file with missing values, duplicates, and varied phone formats.
    This is useful for testing and demonstration purposes.
    
    Args:
        output_path: Path where the sample CSV will be saved
    """
    sample_data = {
        'customer_id': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'first_name': ['Alice', 'Bob', 'Carol', '', 'Eve', 'Alice', 'Frank', 'Grace', 'Henry', ''],
        'last_name': ['Smith', 'Jones', '', 'Davis', 'Miller', 'Smith', 'Brown', 'Wilson', 'Taylor', 'Anderson'],
        'email': ['ALICE@example.com', 'bob@example.com', 'carol@example.com', 'davis@example.com', 
                  'eve@example.com', 'alice@example.com', 'frank@example.com', 'grace@example.com', 
                  'henry@example.com', ''],
        'phone': ['(555) 123-4567', '1-555-234-5678', '555.345.6789', '', 
                  '+44 20 7946 0958', '5551234567', '(555) 987-6543', '555-111-2222',
                  '1-800-555-1234', '12345'],
        'address': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '321 Elm St', 
                    '654 Maple Dr', '123 Main St', '987 Cedar Ln', '', '147 Birch Way', '258 Spruce Ct'],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'London', 
                 'New York', 'Phoenix', 'Philadelphia', 'San Antonio', ''],
        'account_balance': ['1000.50', '2500.00', '', '500.25', '7500.75', 
                           '1000.50', '3200.00', '1500.00', '', '900.00']
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv(output_path, index=False)
    print(f"[OK] Sample CSV generated: {output_path}")
    print(f"  Total rows: {len(df)}")
    print(f"  Contains: missing values, duplicates, and varied phone formats")


# --------------
# Main execution and demonstration
# --------------

def main():
    """
    Main function to demonstrate the CSV cleaning pipeline.
    Generates a sample CSV, processes it, and saves the cleaned output.
    """
    import os
    
    print("=" * 60)
    print("Bank Customer CSV Cleaning Pipeline")
    print("=" * 60)
    print()
    
    # Step 1: Generate sample CSV with issues
    input_file = 'customers_raw.csv'
    print("Step 1: Generating sample CSV with missing values, duplicates, and varied phone formats...")
    generate_sample_csv(input_file)
    print()
    
    # Step 2: Process the CSV
    output_file = 'customers_cleaned.csv'
    print("Step 2: Processing CSV...")
    print("  - Cleaning missing values")
    print("  - Removing duplicates")
    print("  - Standardizing phone numbers")
    print()
    
    # Process with specific requirements
    process_csv(
        in_path=input_file,
        out_path=output_file,
        required_fields=['first_name', 'last_name', 'email'],  # Drop rows missing these
        fill_values={'account_balance': '0.00'},  # Fill missing balances with 0.00
        dedupe_subset=['email', 'phone'],  # Remove duplicates based on email and phone
        phone_field='phone',
        default_country='US'
    )
    print()
    
    # Step 3: Display summary statistics
    print("Step 3: Summary Statistics")
    print("-" * 60)
    df_raw = load_csv(input_file)
    df_cleaned = load_csv(output_file)
    
    print(f"Original CSV: {input_file}")
    print(f"  - Total rows: {len(df_raw)}")
    print(f"  - Missing first_name: {(df_raw['first_name'] == '').sum()}")
    print(f"  - Missing last_name: {(df_raw['last_name'] == '').sum()}")
    print(f"  - Missing email: {(df_raw['email'] == '').sum()}")
    print(f"  - Missing phone: {(df_raw['phone'] == '').sum()}")
    print()
    
    print(f"Cleaned CSV: {output_file}")
    print(f"  - Total rows: {len(df_cleaned)}")
    print(f"  - Rows removed: {len(df_raw) - len(df_cleaned)}")
    print(f"  - Missing first_name: {(df_cleaned['first_name'] == '').sum()}")
    print(f"  - Missing last_name: {(df_cleaned['last_name'] == '').sum()}")
    print(f"  - Missing email: {(df_cleaned['email'] == '').sum()}")
    print(f"  - Missing phone: {(df_cleaned['phone'] == '').sum()}")
    print()
    
    print("Sample of cleaned phone numbers:")
    for idx, phone in enumerate(df_cleaned['phone'].head(5), 1):
        if phone:
            print(f"  {idx}. {phone}")
    print()
    
    print("=" * 60)
    print("[OK] Processing complete!")
    print(f"[OK] Input file:  {input_file}")
    print(f"[OK] Output file: {output_file}")
    print("=" * 60)


# --------------
# Unit Testcases
# --------------

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        # Sample data with missing values, duplicates, and varied phone formats
        self.raw = pd.DataFrame([
            {'customer_id': '1', 'first_name': 'Alice', 'last_name': 'Smith', 'email': 'ALICE@example.com', 'phone': '(555) 123-4567'},
            {'customer_id': '2', 'first_name': 'Bob', 'last_name': 'Jones', 'email': 'bob@example.com', 'phone': '1-555-234-5678'},
            {'customer_id': '3', 'first_name': 'Carol', 'last_name': '', 'email': 'carol@example.com', 'phone': '555.345.6789'},
            {'customer_id': '4', 'first_name': '', 'last_name': 'Davis', 'email': 'davis@example.com', 'phone': ''},  # missing first name
            {'customer_id': '5', 'first_name': 'Eve', 'last_name': 'Miller', 'email': 'eve@example.com', 'phone': '+44 20 7946 0958'},
            {'customer_id': '6', 'first_name': 'Alice', 'last_name': 'Smith', 'email': 'alice@example.com', 'phone': '5551234567'},  # duplicate of id=1 by email/phone
            {'customer_id': '', 'first_name': 'NoID', 'last_name': 'User', 'email': 'noid@example.com', 'phone': '12345'}  # short phone
        ])

    def test_clean_missing_values(self):
        # require first_name and last_name
        cleaned = clean_missing_values(self.raw, required_fields=['first_name', 'last_name'])
        # Rows with missing first or last name should be dropped: id=4 and id=3 (last_name empty)
        ids = set(cleaned['customer_id'])
        self.assertNotIn('3', ids)
        self.assertNotIn('4', ids)

    def test_remove_duplicates_by_email(self):
        # After normalizing email, id=1 and id=6 are duplicates (alice)
        dedup = remove_duplicates(self.raw, subset=['email'])
        emails = [normalize_email(e) for e in dedup['email'].tolist()]
        # should contain 'alice@example.com' only once
        self.assertEqual(emails.count('alice@example.com'), 1)

    def test_standardize_phone_numbers(self):
        df = standardize_phone_numbers(self.raw.copy(), phone_field='phone')
        # Check US style numbers became +1-AAA-BBB-CCCC
        row1 = df[df['customer_id'] == '1'].iloc[0]
        self.assertEqual(row1['phone'], '+1-555-123-4567')
        row2 = df[df['customer_id'] == '2'].iloc[0]
        self.assertEqual(row2['phone'], '+1-555-234-5678')
        # UK number should preserve country code +44 and format to +44-020-794-60958 -> our rule formats as last 10 digits:
        row5 = df[df['customer_id'] == '5'].iloc[0]
        # The input +44 20 7946 0958 becomes digits '442079460958' -> country='44', subscriber='2079460958' -> +44-207-946-0958
        self.assertEqual(row5['phone'], '+44-207-946-0958')
        # Short phone stays digits-only
        row7 = df[df['customer_id'] == '7']
        # there's no customer_id '7' in sample; short phone has customer_id '' (empty string)
        short = df[df['customer_id'] == '']['phone'].iloc[0]
        self.assertEqual(short, '12345')

    def test_full_pipeline(self):
        processed = process_dataframe(self.raw,
                                      required_fields=['first_name', 'last_name', 'email'],
                                      fill_values={'phone': ''},
                                      dedupe_subset=['email', 'phone'],
                                      phone_field='phone')
        # Ensure no missing requireds
        self.assertTrue((processed['first_name'] != '').all())
        self.assertTrue((processed['last_name'] != '').all())
        self.assertTrue((processed['email'] != '').all())
        # Ensure duplicates (alice) reduced to one
        self.assertEqual(sum(normalize_email(e) == 'alice@example.com' for e in processed['email']), 1)
        # Ensure phones standardized
        self.assertTrue(all(p == '' or p.startswith('+') or p.isdigit() for p in processed['phone']))

if __name__ == '__main__':
    import sys
    
    # Check if user wants to run tests or demo
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Run unit tests
        print("Running unit tests...")
        print("=" * 60)
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        # Run main demonstration
        try:
            main()
        except Exception as e:
            print(f"\n[ERROR] Error: {e}")
            print("\nTo run unit tests instead, use: python TASK1.PY --test")
            sys.exit(1)