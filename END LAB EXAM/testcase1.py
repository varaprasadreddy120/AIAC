"""
Unit Tests for Bank Customer Data Processing
=============================================

Comprehensive test suite for customer data cleaning, deduplication, 
and phone number standardization functions.

Test Coverage:
--------------
1. Missing Value Cleaning Tests
2. Duplicate Removal Tests
3. Phone Number Standardization Tests
4. CSV Processing Integration Tests
5. Data Integrity Tests
6. Edge Case Tests

Author: THALLAPELLI SAVIN KUMAR
Date: 20-Nov-2025
"""

import unittest
import pandas as pd
import tempfile
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def clean_missing_values(df, strategy="drop"):
    """Clean missing values in the DataFrame."""
    if strategy == "drop":
        return df.dropna()
    elif strategy == "fill":
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("")
            else:
                df[col] = df[col].fillna(0)
        return df
    else:
        raise ValueError("Invalid strategy. Choose 'drop' or 'fill'.")


def remove_duplicates(df):
    """Remove duplicate records based on all columns."""
    return df.drop_duplicates()


def standardize_phone_number(phone):
    """Standardize phone number to format: +91-XXXXXXXXXX"""
    import re
    if pd.isna(phone):
        return ""
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return "+91-" + digits
    elif len(digits) == 12 and digits.startswith("91"):
        return "+91-" + digits[2:]
    else:
        return ""


def standardize_phone_numbers(df, phone_col="Phone"):
    """Apply phone number standardization to a DataFrame column."""
    if phone_col in df.columns:
        df[phone_col] = df[phone_col].apply(standardize_phone_number)
    else:
        print(f"Warning: Phone column '{phone_col}' not found.")
    return df


class TestCleanMissingValues(unittest.TestCase):
    """Test cases for clean_missing_values function"""
    
    def setUp(self):
        """Create sample DataFrames for testing"""
        self.df_with_nulls = pd.DataFrame({
            "CustomerID": [101, 102, 103, None],
            "Name": ["Alice", None, "Charlie", "David"],
            "Email": ["alice@mail.com", "bob@mail.com", None, "david@mail.com"],
            "Balance": [1000, 2000, None, 3000]
        })
        
        self.df_no_nulls = pd.DataFrame({
            "CustomerID": [101, 102, 103],
            "Name": ["Alice", "Bob", "Charlie"],
            "Balance": [1000, 2000, 3000]
        })
    
    def test_drop_strategy_removes_rows_with_nulls(self):
        """Test that drop strategy removes all rows with any null values"""
        result = clean_missing_values(self.df_with_nulls, strategy="drop")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["Name"], "Alice")
    
    def test_fill_strategy_fills_object_columns(self):
        """Test that fill strategy fills object columns with empty string"""
        result = clean_missing_values(self.df_with_nulls, strategy="fill")
        self.assertEqual(result.iloc[1]["Name"], "")
        self.assertEqual(result.iloc[2]["Email"], "")
    
    def test_fill_strategy_fills_numeric_columns(self):
        """Test that fill strategy fills numeric columns with 0"""
        result = clean_missing_values(self.df_with_nulls, strategy="fill")
        self.assertEqual(result.iloc[3]["CustomerID"], 0)
        self.assertEqual(result.iloc[2]["Balance"], 0)
    
    def test_invalid_strategy_raises_error(self):
        """Test that invalid strategy raises ValueError"""
        with self.assertRaises(ValueError):
            clean_missing_values(self.df_with_nulls, strategy="invalid")
    
    def test_no_missing_values_unchanged(self):
        """Test that DataFrame with no missing values remains unchanged"""
        result = clean_missing_values(self.df_no_nulls, strategy="drop")
        self.assertEqual(len(result), 3)
        pd.testing.assert_frame_equal(result, self.df_no_nulls)
    
    def test_fill_preserves_existing_data(self):
        """Test that fill strategy preserves existing valid data"""
        result = clean_missing_values(self.df_with_nulls, strategy="fill")
        self.assertEqual(result.iloc[0]["Name"], "Alice")
        self.assertEqual(result.iloc[0]["Balance"], 1000)


class TestRemoveDuplicates(unittest.TestCase):
    """Test cases for remove_duplicates function"""
    
    def setUp(self):
        """Create sample DataFrames for testing"""
        self.df_with_duplicates = pd.DataFrame({
            "CustomerID": [101, 102, 102, 103],
            "Name": ["Alice", "Bob", "Bob", "Charlie"],
            "Phone": ["9876543210", "8765432101", "8765432101", "7654321098"]
        })
        
        self.df_no_duplicates = pd.DataFrame({
            "CustomerID": [101, 102, 103],
            "Name": ["Alice", "Bob", "Charlie"]
        })
        
        self.df_all_duplicates = pd.DataFrame({
            "CustomerID": [101, 101, 101],
            "Name": ["Alice", "Alice", "Alice"]
        })
    
    def test_remove_exact_duplicates(self):
        """Test removing completely identical rows"""
        result = remove_duplicates(self.df_with_duplicates)
        self.assertEqual(len(result), 3)
    
    def test_no_duplicates_unchanged(self):
        """Test that DataFrame with no duplicates remains unchanged"""
        result = remove_duplicates(self.df_no_duplicates)
        self.assertEqual(len(result), 3)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), 
                                      self.df_no_duplicates.reset_index(drop=True))
    
    def test_all_duplicates_keeps_one(self):
        """Test that all duplicate rows are reduced to one"""
        result = remove_duplicates(self.df_all_duplicates)
        self.assertEqual(len(result), 1)
    
    def test_first_occurrence_preserved(self):
        """Test that first occurrence of duplicate is preserved"""
        result = remove_duplicates(self.df_with_duplicates)
        self.assertIn(102, result["CustomerID"].values)


class TestStandardizePhoneNumber(unittest.TestCase):
    """Test cases for standardize_phone_number function"""
    
    def test_10_digit_phone(self):
        """Test standardizing 10-digit phone number"""
        result = standardize_phone_number("9876543210")
        self.assertEqual(result, "+91-9876543210")
    
    def test_phone_with_country_code_prefix(self):
        """Test phone number starting with 91"""
        result = standardize_phone_number("91-9876543210")
        self.assertEqual(result, "+91-9876543210")
    
    def test_phone_with_dashes(self):
        """Test phone number with dashes"""
        result = standardize_phone_number("98765-43210")
        self.assertEqual(result, "+91-9876543210")
    
    def test_phone_with_spaces(self):
        """Test phone number with spaces"""
        result = standardize_phone_number("9876 543 210")
        self.assertEqual(result, "+91-9876543210")
    
    def test_phone_with_parentheses(self):
        """Test phone number with parentheses"""
        result = standardize_phone_number("(9876) 543-210")
        self.assertEqual(result, "+91-9876543210")
    
    def test_phone_with_mixed_separators(self):
        """Test phone with mixed separators"""
        result = standardize_phone_number("+91 (9876) 543-210")
        self.assertEqual(result, "+91-9876543210")
    
    def test_invalid_short_phone(self):
        """Test that short invalid phone returns empty string"""
        result = standardize_phone_number("12345")
        self.assertEqual(result, "")
    
    def test_invalid_long_phone(self):
        """Test that too long phone returns empty string"""
        result = standardize_phone_number("123456789012345")
        self.assertEqual(result, "")
    
    def test_null_phone(self):
        """Test that null/NaN phone returns empty string"""
        result = standardize_phone_number(None)
        self.assertEqual(result, "")
    
    def test_nan_phone(self):
        """Test that NaN phone returns empty string"""
        result = standardize_phone_number(pd.NA)
        self.assertEqual(result, "")
    
    def test_empty_string_phone(self):
        """Test empty string phone"""
        result = standardize_phone_number("")
        self.assertEqual(result, "")


class TestStandardizePhoneNumbers(unittest.TestCase):
    """Test cases for standardize_phone_numbers function"""
    
    def test_standardize_phone_column(self):
        """Test standardizing Phone column in DataFrame"""
        df = pd.DataFrame({
            "CustomerID": [1, 2, 3],
            "Phone": ["9876543210", "91-8765432101", "8765432101"]
        })
        result = standardize_phone_numbers(df, phone_col="Phone")
        self.assertEqual(result.iloc[0]["Phone"], "+91-9876543210")
        self.assertEqual(result.iloc[1]["Phone"], "+91-8765432101")
        self.assertEqual(result.iloc[2]["Phone"], "+91-8765432101")
    
    def test_missing_column_warning(self):
        """Test that missing column triggers warning"""
        df = pd.DataFrame({
            "CustomerID": [1, 2],
            "Name": ["Alice", "Bob"]
        })
        # Should not raise error, just print warning
        result = standardize_phone_numbers(df, phone_col="Phone")
        self.assertIsNotNone(result)
    
    def test_custom_column_name(self):
        """Test with custom column name"""
        df = pd.DataFrame({
            "CustomerID": [1, 2],
            "MobileNo": ["9876543210", "8765432101"]
        })
        result = standardize_phone_numbers(df, phone_col="MobileNo")
        self.assertEqual(result.iloc[0]["MobileNo"], "+91-9876543210")
    
    def test_handles_null_values_in_column(self):
        """Test that null values in column are handled"""
        df = pd.DataFrame({
            "Phone": ["9876543210", None, "8765432101"]
        })
        result = standardize_phone_numbers(df, phone_col="Phone")
        self.assertEqual(result.iloc[0]["Phone"], "+91-9876543210")
        self.assertEqual(result.iloc[1]["Phone"], "")
        self.assertEqual(result.iloc[2]["Phone"], "+91-8765432101")


class TestIntegrationPipeline(unittest.TestCase):
    """Integration tests for the complete pipeline"""
    
    def setUp(self):
        """Create sample data for integration testing"""
        self.sample_data = pd.DataFrame({
            "CustomerID": [101, 102, 102, 103, 104, 105],
            "Name": ["Alice", "Bob", "Bob", None, "Eve", "Frank"],
            "Phone": ["9876543210", "91-8765432101", "8765432101", "12345", None, "98765-43210"],
            "Balance": [1000, 2000, 2000, 1500, None, 3000]
        })
    
    def test_full_pipeline_drop_strategy(self):
        """Test complete pipeline with drop strategy"""
        df = self.sample_data.copy()
        df_clean = clean_missing_values(df, strategy="drop")
        df_unique = remove_duplicates(df_clean)
        df_final = standardize_phone_numbers(df_unique, phone_col="Phone")
        
        # Should have fewer records due to dropping nulls
        self.assertLess(len(df_final), len(self.sample_data))
        # All names should be non-null
        self.assertTrue(df_final["Name"].notna().all())
    
    def test_full_pipeline_fill_strategy(self):
        """Test complete pipeline with fill strategy"""
        df = self.sample_data.copy()
        df_clean = clean_missing_values(df, strategy="fill")
        df_unique = remove_duplicates(df_clean)
        df_final = standardize_phone_numbers(df_unique, phone_col="Phone")
        
        # Should preserve all records from fill strategy
        self.assertGreaterEqual(len(df_final), 3)
        # Phone numbers should be standardized
        valid_phones = df_final[df_final["Phone"].notna()]
        for phone in valid_phones["Phone"]:
            if phone:  # if not empty string
                self.assertTrue(phone.startswith("+91-"))
    
    def test_data_preserved_through_pipeline(self):
        """Test that customer data is preserved through pipeline"""
        df = self.sample_data.copy()
        original_ids = set(df["CustomerID"].dropna())
        
        df_clean = clean_missing_values(df, strategy="fill")
        df_unique = remove_duplicates(df_clean)
        df_final = standardize_phone_numbers(df_unique, phone_col="Phone")
        
        final_ids = set(df_final["CustomerID"].dropna())
        # Original IDs should be subset of final IDs
        self.assertTrue(original_ids.issubset(final_ids))


class TestCSVProcessing(unittest.TestCase):
    """Test CSV file processing"""
    
    def test_csv_read_write(self):
        """Test reading and writing CSV files"""
        df = pd.DataFrame({
            "CustomerID": [101, 102],
            "Name": ["Alice", "Bob"],
            "Phone": ["9876543210", "8765432101"],
            "Balance": [1000, 2000]
        })
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            # Write CSV
            df.to_csv(temp_path, index=False)
            
            # Read CSV
            df_read = pd.read_csv(temp_path)
            
            # Verify data integrity
            self.assertEqual(len(df_read), 2)
            self.assertIn("CustomerID", df_read.columns)
            self.assertEqual(df_read.iloc[0]["Name"], "Alice")
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_process_and_save_cleaned_csv(self):
        """Test processing CSV and saving cleaned version"""
        df = pd.DataFrame({
            "CustomerID": [101, 102, 102],
            "Name": ["Alice", None, "Bob"],
            "Phone": ["9876543210", "8765432101", "8765432101"],
            "Balance": [1000, 2000, 2000]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            input_path = f.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            output_path = f.name
        
        try:
            # Write input CSV
            df.to_csv(input_path, index=False)
            
            # Process
            df_input = pd.read_csv(input_path)
            df_clean = clean_missing_values(df_input, strategy="fill")
            df_unique = remove_duplicates(df_clean)
            df_final = standardize_phone_numbers(df_unique, phone_col="Phone")
            
            # Write output
            df_final.to_csv(output_path, index=False)
            
            # Verify
            df_output = pd.read_csv(output_path)
            self.assertGreaterEqual(len(df_output), 2)
        finally:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity through processing"""
    
    def test_no_data_loss_in_fill(self):
        """Test that fill strategy doesn't lose data"""
        df = pd.DataFrame({
            "ID": [1, 2, 3],
            "Value": [100, None, 300]
        })
        result = clean_missing_values(df, strategy="fill")
        self.assertEqual(len(result), len(df))
    
    def test_column_structure_preserved(self):
        """Test that column structure is preserved"""
        df = pd.DataFrame({
            "CustomerID": [101, 102],
            "Name": ["Alice", "Bob"],
            "Phone": ["9876543210", "8765432101"],
            "Balance": [1000, 2000]
        })
        
        df_clean = clean_missing_values(df, strategy="fill")
        df_unique = remove_duplicates(df_clean)
        df_final = standardize_phone_numbers(df_unique, phone_col="Phone")
        
        original_cols = set(df.columns)
        final_cols = set(df_final.columns)
        self.assertEqual(original_cols, final_cols)
    
    def test_data_types_preserved(self):
        """Test that data types are appropriate after processing"""
        df = pd.DataFrame({
            "CustomerID": [101, 102],
            "Balance": [1000, 2000]
        })
        result = clean_missing_values(df, strategy="fill")
        self.assertEqual(result["CustomerID"].dtype, df["CustomerID"].dtype)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame"""
        df = pd.DataFrame()
        result = clean_missing_values(df, strategy="drop")
        self.assertEqual(len(result), 0)
    
    def test_single_row_dataframe(self):
        """Test with single row"""
        df = pd.DataFrame({
            "Name": ["Alice"],
            "Phone": ["9876543210"]
        })
        result = remove_duplicates(df)
        self.assertEqual(len(result), 1)
    
    def test_all_null_values(self):
        """Test with all null values"""
        df = pd.DataFrame({
            "Col1": [None, None, None],
            "Col2": [None, None, None]
        })
        result = clean_missing_values(df, strategy="drop")
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)