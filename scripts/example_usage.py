"""
Example Usage of Reusable Modules

This script demonstrates how to use the modular data processing functions
instead of procedural code in notebooks.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import SolarDataLoader, load_solar_data
from src.data_cleaner import SolarDataCleaner, clean_solar_data
from src.data_exporter import SolarDataExporter, export_cleaned_data


def example_using_classes():
    """Example using class-based approach"""
    print("=" * 80)
    print("Example 1: Using Classes")
    print("=" * 80)
    
    # Step 1: Load data using class
    data_path = Path('data/benin-malanville.csv')
    loader = SolarDataLoader(data_path)
    df = loader.load()
    
    # Get dataset information
    info = loader.get_info()
    print(f"\nDataset loaded: {info['shape']}")
    print(f"Date range: {info['date_range']}")
    
    # Step 2: Clean data using class
    cleaner = SolarDataCleaner(df)
    
    # Define columns for cleaning
    numeric_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 'WS', 'WSgust']
    outlier_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
    
    # Perform cleaning
    df_cleaned = cleaner.clean(
        numeric_columns=numeric_cols,
        outlier_columns=outlier_cols,
        imputation_method='median',
        z_threshold=3.0
    )
    
    # Get cleaning report
    report = cleaner.get_cleaning_report()
    print(f"\nCleaning completed:")
    print(f"  - Missing values imputed: {len(numeric_cols)} columns")
    print(f"  - Outliers detected: {report.get('total_outliers', 0)} rows")
    
    # Step 3: Export cleaned data
    exporter = SolarDataExporter(df_cleaned)
    output_path = exporter.export(
        'data/benin_clean_example.csv',
        remove_temp=True,
        index=False
    )
    print(f"\nCleaned data exported to: {output_path}")


def example_using_functions():
    """Example using convenience functions"""
    print("\n" + "=" * 80)
    print("Example 2: Using Convenience Functions")
    print("=" * 80)
    
    # Step 1: Load data
    df = load_solar_data('data/benin-malanville.csv')
    print(f"\nData loaded: {df.shape}")
    
    # Step 2: Clean data
    outlier_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
    df_cleaned, report = clean_solar_data(
        df,
        numeric_columns=['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 'WS', 'WSgust'],
        outlier_columns=outlier_cols,
        imputation_method='median',
        z_threshold=3.0
    )
    
    print(f"\nCleaning report:")
    print(f"  - Total outliers: {report.get('total_outliers', 0)}")
    
    # Step 3: Export
    output_path = export_cleaned_data(
        df_cleaned,
        'data/benin_clean_function_example.csv',
        remove_temp=True
    )
    print(f"\nExported to: {output_path}")


def example_minimal_workflow():
    """Example of minimal workflow for quick processing"""
    print("\n" + "=" * 80)
    print("Example 3: Minimal Workflow")
    print("=" * 80)
    
    # Load, clean, and export in minimal steps
    df = load_solar_data('data/benin-malanville.csv')
    
    df_cleaned, _ = clean_solar_data(
        df,
        outlier_columns=['GHI', 'DNI', 'DHI']
    )
    
    export_cleaned_data(df_cleaned, 'data/benin_clean_minimal.csv')
    print("\nMinimal workflow completed!")


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("Solar Data Processing - Example Usage")
    print("=" * 80)
    print("\nThis script demonstrates reusable modules for:")
    print("  1. Loading solar data")
    print("  2. Cleaning data (missing values, outliers)")
    print("  3. Exporting cleaned datasets")
    print("\nNote: Make sure data files exist in the data/ directory")
    print("=" * 80)
    
    # Uncomment the example you want to run:
    # example_using_classes()
    # example_using_functions()
    # example_minimal_workflow()
    
    print("\nTo run examples, uncomment the function calls in the script.")

