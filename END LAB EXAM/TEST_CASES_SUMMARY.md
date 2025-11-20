# Test Cases Summary

## TASK1.PY - Bank Customer CSV Cleaning

### Test Suite: `TestDataProcessing`
**Total Tests: 4** | **Status: ✅ All Passing**

---

#### 1. `test_clean_missing_values`
**Purpose:** Tests missing value cleaning functionality

**Test Data:**
- 7 customer records with various missing values
- Missing first_name (customer_id: '4')
- Missing last_name (customer_id: '3')

**Test Logic:**
- Requires `first_name` and `last_name` fields
- Verifies that rows with missing required fields are dropped
- Checks that customer_id '3' and '4' are removed from cleaned data

**Expected Result:** ✅ Rows with missing required fields are successfully removed

---

#### 2. `test_remove_duplicates_by_email`
**Purpose:** Tests duplicate removal based on email normalization

**Test Data:**
- Customer '1' with email: 'ALICE@example.com'
- Customer '6' with email: 'alice@example.com' (duplicate, different case)

**Test Logic:**
- Normalizes emails (case-insensitive)
- Removes duplicates based on email field
- Verifies 'alice@example.com' appears only once after deduplication

**Expected Result:** ✅ Duplicate emails are detected and removed (case-insensitive)

---

#### 3. `test_standardize_phone_numbers`
**Purpose:** Tests phone number standardization to E.164-like format

**Test Cases:**
- US format: `(555) 123-4567` → `+1-555-123-4567`
- US format with country code: `1-555-234-5678` → `+1-555-234-5678`
- UK format: `+44 20 7946 0958` → `+44-207-946-0958`
- Short number: `12345` → `12345` (preserved as-is)

**Expected Result:** ✅ All phone numbers are standardized correctly

---

#### 4. `test_full_pipeline`
**Purpose:** Tests the complete data cleaning pipeline end-to-end

**Test Logic:**
- Applies all cleaning steps: missing values, duplicates, phone standardization
- Verifies:
  - No missing values in required fields (first_name, last_name, email)
  - Duplicates removed (alice@example.com appears only once)
  - Phone numbers are standardized (start with '+' or are digits)

**Expected Result:** ✅ Complete pipeline works correctly with all features combined

---

## TASK2.PY - Gaming Leaderboard Quick Sort

### Test Suite: `TestQuickSortLeaderboard`
**Total Tests: 7** | **Status: ✅ All Passing**

---

#### 1. `test_empty`
**Purpose:** Tests Quick Sort with empty list (edge case)

**Test Data:** Empty list `[]`

**Expected Result:** ✅ Returns empty list without errors

---

#### 2. `test_single`
**Purpose:** Tests Quick Sort with single element (edge case)

**Test Data:** Single player `Player("Alice", 100)`

**Expected Result:** ✅ Returns the same single element unchanged

---

#### 3. `test_basic_descending`
**Purpose:** Tests basic descending sort (leaderboard style - highest first)

**Test Data:**
- Alice: 150
- Bob: 200
- Carol: 100

**Expected Order:** Bob (200) → Alice (150) → Carol (100)

**Expected Result:** ✅ Players sorted correctly in descending order

---

#### 4. `test_basic_ascending`
**Purpose:** Tests basic ascending sort (lowest to highest)

**Test Data:**
- Alice: 150
- Bob: 200
- Carol: 100

**Expected Order:** Carol (100) → Alice (150) → Bob (200)

**Expected Result:** ✅ Players sorted correctly in ascending order

---

#### 5. `test_ties_preserve_order`
**Purpose:** Tests stability - players with equal scores preserve original order

**Test Data:**
- P1: 100
- P2: 200
- P3: 100 (same as P1)
- P4: 200 (same as P2)

**Expected Order:** P2 → P4 → P1 → P3
- 200s in original order (P2 before P4)
- 100s in original order (P1 before P3)

**Expected Result:** ✅ Stability preserved - equal scores maintain relative order

---

#### 6. `test_random_compare_builtin_sorted`
**Purpose:** Validates Quick Sort correctness against Python's built-in sorted

**Test Data:**
- 200 randomly generated players with scores 0-1000
- Uses fixed random seed for reproducibility

**Test Logic:**
- Compares our Quick Sort output with Python's `sorted()`
- Verifies score sequences match
- Ensures stability is maintained for equal scores

**Expected Result:** ✅ Quick Sort produces identical results to Python's sorted

---

#### 7. `test_non_player_items_with_key`
**Purpose:** Tests Quick Sort with non-Player objects using custom key function

**Test Data:**
- Dictionary objects: `{"name": "A", "score": 10}`, etc.

**Test Logic:**
- Uses custom key function: `lambda x: x["score"]`
- Sorts by score in descending order

**Expected Order:** B (30) → C (20) → A (10)

**Expected Result:** ✅ Quick Sort works with any comparable objects using key function

---

## Running Tests

### TASK1.PY Tests
```bash
python TASK1.PY --test
```

**Output:**
```
Running unit tests...
============================================================
test_clean_missing_values ... ok
test_full_pipeline ... ok
test_remove_duplicates_by_email ... ok
test_standardize_phone_numbers ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.015s

OK
```

### TASK2.PY Tests
```bash
python TASK2.PY --test
```

**Output:**
```
Running unit tests...
======================================================================
test_basic_ascending ... ok
test_basic_descending ... ok
test_empty ... ok
test_non_player_items_with_key ... ok
test_random_compare_builtin_sorted ... ok
test_single ... ok
test_ties_preserve_order ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```

---

## Test Coverage Summary

### TASK1.PY Coverage:
- ✅ Missing value handling
- ✅ Duplicate detection and removal
- ✅ Phone number standardization (multiple formats)
- ✅ End-to-end pipeline integration
- ✅ Edge cases (empty fields, various formats)

### TASK2.PY Coverage:
- ✅ Empty and single-element lists (edge cases)
- ✅ Ascending and descending sort
- ✅ Stability (equal elements preserve order)
- ✅ Large random datasets (200 elements)
- ✅ Custom key functions
- ✅ Comparison with standard library

---

## All Tests Status: ✅ PASSING

**Total Test Cases: 11**
- TASK1.PY: 4 tests ✅
- TASK2.PY: 7 tests ✅

**Execution Time:** < 0.02 seconds for all tests

