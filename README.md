# Data Processing & Cleansing Utility

A modular Python utility developed to read tabular employee records from Excel formats, perform schema validation, apply standard column mappings, and export cleaned datasets to CSV formats with built-in error handling and automated testing.

---

## Overview

This project was built during the Software Engineering & Data fundamentals training (Week 1). It focuses on transitioning procedural scripts into production-ready, clean Python code following PEP 8 standards, complete with logging, custom error handling, and unit testing via `pytest`.

---

## Key Features & Code Logic

The main module `data_processor.py` provides the following capabilities:

1. **Dual Excel Ingestion:**
   - `data_reader()`: Ingests Excel worksheets directly into a Pandas `DataFrame`.
   - `data_reader_openpyxl()`: Reads raw cell values row-by-row using `openpyxl` as a secondary fallback.

2. **Column Validation & Renaming:**
   - `check_columns_exist()`: Checks whether a specific column or a list of target columns exist in the DataFrame, returning a status dictionary.
   - `rename_columns()`: Safely maps and renames columns according to a provided schema. Raises an explicit `KeyError` if any target column is missing.

3. **CSV Exporting:**
   - `data_writer()`: Exports processed DataFrames to clean CSV files with standard UTF-8 encoding.

4. **Logging & Error Raising:**
   - Replaced basic print statements with Python's built-in `logging` module to track process states (`INFO`, `ERROR`).
   - Guarded against script-level execution leaks using `if __name__ == "__main__":`.

---

## Automated Unit Testing (`pytest`)

All tests are located in `test_data_processor.py` and run against in-memory fixture data (completely isolated from external files or network calls):

- **Positive Case (`test_rename_columns_positive`):** Verifies successful column name transformation against an in-memory sample DataFrame.
- **Negative Case (`test_rename_columns_negative`):** Asserts that attempting to rename a non-existing column triggers an explicit `KeyError` via `pytest.raises`.
- **Edge/Mixed Case (`test_check_columns_exist_mixed`):** Verifies that `check_columns_exist` accurately returns `True` for existing columns and `False` for missing columns simultaneously.

---
