# Source Code Modules

This directory contains reusable, modular code for solar data processing. The modules are designed to replace procedural notebook code with reusable functions and classes.

## Table of Contents

- [Modules Overview](#modules-overview)
- [Detailed Usage Examples](#detailed-usage-examples)
- [Expected Inputs and Outputs](#expected-inputs-and-outputs)
- [API Reference](#api-reference)
- [Usage in Notebooks](#usage-in-notebooks)
- [Running Tests](#running-tests)

## Modules Overview

### `data_loader.py`
Handles loading and preprocessing of solar data files.

**Classes:**
- `SolarDataLoader`: Class for loading and managing solar data

**Functions:**
- `load_solar_data()`: Convenience function to load data

### `data_cleaner.py`
Handles data cleaning operations including missing value imputation and outlier detection/treatment.

**Classes:**
- `SolarDataCleaner`: Class for cleaning solar data

**Functions:**
- `clean_solar_data()`: Convenience function to clean data

### `data_exporter.py`
Handles exporting cleaned datasets to CSV files.

**Classes:**
- `SolarDataExporter`: Class for exporting data

**Functions:**
- `export_cleaned_data()`: Convenience function to export data

## Detailed Usage Examples

### Example 1: Complete Data Processing Pipeline

```python
from src import load_solar_data, clean_solar_data, export_cleaned_data

# Step 1: Load data
# Input: Path to CSV file (str or Path)
# Output: DataFrame with Timestamp converted to datetime
df = load_solar_data('data/benin-malanville.csv')
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
# Output: Loaded 525600 rows, 19 columns

# Step 2: Clean data
# Input: DataFrame, list of columns, z-score threshold
# Output: Tuple of (cleaned DataFrame, cleaning report dictionary)
df_cleaned, report = clean_solar_data(
    df,
    numeric_columns=['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 'WS', 'WSgust'],
    outlier_columns=['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust'],
    imputation_method='median',
    z_threshold=3.0
)

# Access cleaning report
print(f"Outliers detected: {report['total_outliers']} rows")
print(f"Missing values imputed: {len(report['missing_values']['missing_by_column'])} columns")
# Output: Outliers detected: 7740 rows
# Output: Missing values imputed: 9 columns

# Step 3: Export cleaned data
# Input: DataFrame, output path, options
# Output: Path object pointing to exported file
output_path = export_cleaned_data(
    df_cleaned,
    'data/benin_clean.csv',
    remove_temp=True,
    index=False
)
print(f"Exported to: {output_path}")
# Output: Exported to: data/benin_clean.csv
```

### Example 2: Using Classes for More Control

```python
from src.data_loader import SolarDataLoader
from src.data_cleaner import SolarDataCleaner
from src.data_exporter import SolarDataExporter

# Load with class
loader = SolarDataLoader('data/benin-malanville.csv')
df = loader.load()
info = loader.get_info()
print(f"Date range: {info['date_range'][0]} to {info['date_range'][1]}")

# Clean with class
cleaner = SolarDataCleaner(df)
df_cleaned = cleaner.clean(
    numeric_columns=['GHI', 'DNI', 'DHI'],
    outlier_columns=['GHI', 'DNI', 'DHI'],
    z_threshold=3.0
)
cleaning_report = cleaner.get_cleaning_report()

# Export with class
exporter = SolarDataExporter(df_cleaned)
exporter.remove_temp_columns(['Outlier_Flag', 'Hour', 'Month'])
output_path = exporter.export('data/benin_clean.csv', remove_temp=False)
```

### Example 3: Handling Missing Values Only

```python
from src.data_cleaner import SolarDataCleaner

cleaner = SolarDataCleaner(df)

# Detect missing values
missing_stats = cleaner.detect_missing_values(threshold=0.05)
print(f"Columns with >5% missing: {list(missing_stats['high_missing_columns'].keys())}")

# Impute only specific columns
df_imputed = cleaner.impute_missing_values(
    columns=['GHI', 'DNI', 'DHI'],
    method='median'
)
```

## Expected Inputs and Outputs

### `load_solar_data()`

**Input:**
- `file_path` (str or Path): Path to CSV file
- `timestamp_col` (str, optional): Name of timestamp column, default='Timestamp'

**Output:**
- `pd.DataFrame`: DataFrame with:
  - All original columns from CSV
  - Timestamp column converted to datetime64
  - Same number of rows as input file

**Example Input:**
```python
file_path = 'data/benin-malanville.csv'
```

**Example Output:**
```python
# DataFrame shape: (525600, 19)
# Columns: ['Timestamp', 'GHI', 'DNI', 'DHI', 'ModA', 'ModB', ...]
# Timestamp dtype: datetime64[ns]
```

### `clean_solar_data()`

**Input:**
- `df` (pd.DataFrame): Input dataframe
- `numeric_columns` (list, optional): Columns to impute, default=all numeric
- `outlier_columns` (list, optional): Columns to check for outliers
- `imputation_method` (str): 'median', 'mean', or 'mode', default='median'
- `z_threshold` (float): Z-score threshold, default=3.0

**Output:**
- `tuple`: (cleaned_dataframe, cleaning_report)
  - `cleaned_dataframe`: pd.DataFrame with:
    - Missing values imputed
    - Outliers capped to ±z_threshold standard deviations
    - 'Outlier_Flag' column added (True for detected outliers)
  - `cleaning_report`: dict with:
    - `missing_values`: Statistics about missing values
    - `outliers`: Dictionary of outlier counts per column
    - `total_outliers`: Total number of rows flagged

**Example Input:**
```python
df = load_solar_data('data/benin-malanville.csv')
numeric_cols = ['GHI', 'DNI', 'DHI']
outlier_cols = ['GHI', 'DNI', 'DHI']
```

**Example Output:**
```python
# cleaned_dataframe: Same shape as input, with cleaned values
# cleaning_report: {
#     'missing_values': {'total_missing': 150, ...},
#     'outliers': {'GHI': {'count': 1200, 'percentage': 0.23}, ...},
#     'total_outliers': 7740
# }
```

### `export_cleaned_data()`

**Input:**
- `df` (pd.DataFrame): Cleaned dataframe to export
- `output_path` (str or Path): Path where to save CSV
- `remove_temp` (bool): Remove temporary columns, default=True
- `temp_columns` (list, optional): List of temp columns to remove
- `index` (bool): Include index in CSV, default=False

**Output:**
- `Path`: Path object pointing to exported file

**Example Input:**
```python
df_cleaned = clean_solar_data(df)[0]
output_path = 'data/benin_clean.csv'
```

**Example Output:**
```python
# Path('data/benin_clean.csv')
# File created with cleaned data, temporary columns removed
```

## API Reference

### `SolarDataLoader` Class

**Methods:**
- `load(timestamp_col='Timestamp')` → pd.DataFrame
- `set_time_index(timestamp_col='Timestamp')` → pd.DataFrame
- `get_info()` → dict

### `SolarDataCleaner` Class

**Methods:**
- `detect_missing_values(threshold=0.05)` → dict
- `impute_missing_values(columns=None, method='median')` → pd.DataFrame
- `detect_outliers(columns, z_threshold=3.0)` → pd.DataFrame
- `cap_outliers(columns, z_threshold=3.0)` → pd.DataFrame
- `clean(numeric_columns=None, outlier_columns=None, ...)` → pd.DataFrame
- `get_cleaning_report()` → dict

### `SolarDataExporter` Class

**Methods:**
- `remove_temp_columns(temp_columns=None)` → pd.DataFrame
- `export(output_path, remove_temp=True, ...)` → Path

## Usage in Notebooks

Instead of procedural code, notebooks can now use these modules:

```python
# Old procedural way:
# df = pd.read_csv('data/benin-malanville.csv')
# df['Timestamp'] = pd.to_datetime(df['Timestamp'])
# ... many lines of cleaning code ...

# New modular way:
from src import load_solar_data, clean_solar_data, export_cleaned_data

df = load_solar_data('data/benin-malanville.csv')
df_cleaned, report = clean_solar_data(df, outlier_columns=['GHI', 'DNI', 'DHI'])
export_cleaned_data(df_cleaned, 'data/benin_clean.csv')
```

## Benefits

1. **Reusability**: Same code can be used across multiple notebooks
2. **Maintainability**: Changes to cleaning logic only need to be made in one place
3. **Testability**: Unit tests can verify module functionality
4. **Modularity**: Each module has a single, clear responsibility
5. **Readability**: Clear function signatures and documentation

## Running Tests

```bash
pytest tests/
```

## Examples

See `scripts/example_usage.py` for complete usage examples.

## Additional Resources

- See `docs/COMMIT_MESSAGE_GUIDE.md` for commit message best practices
- See `docs/STREAMLIT_DASHBOARD.md` for dashboard interface documentation
- See `scripts/cross_country_synthesis.py` for cross-country analysis

