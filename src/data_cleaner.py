"""
Data Cleaning Module

This module provides reusable functions for cleaning solar data, including:
- Missing value imputation
- Outlier detection and treatment
- Data validation
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import List, Optional, Tuple


class SolarDataCleaner:
    """
    A class for cleaning solar irradiance data.
    
    This class handles:
    - Missing value imputation
    - Outlier detection using Z-scores
    - Outlier capping
    - Data quality reporting
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the data cleaner.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe to clean
        """
        self.df = df.copy()
        self.df_cleaned = None
        self.outlier_flags = {}
        self.cleaning_stats = {}
        
    def detect_missing_values(self, threshold: float = 0.05) -> dict:
        """
        Detect missing values and identify columns with >threshold missing.
        
        Parameters:
        -----------
        threshold : float, default 0.05
            Threshold for missing value percentage (5%)
            
        Returns:
        --------
        dict
            Dictionary with missing value statistics
        """
        missing = self.df.isna().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        high_missing = missing_pct[missing_pct > threshold * 100]
        
        stats = {
            'total_missing': missing.sum(),
            'missing_by_column': missing.to_dict(),
            'missing_percentage': missing_pct.to_dict(),
            'high_missing_columns': high_missing.to_dict() if len(high_missing) > 0 else {}
        }
        
        return stats
    
    def impute_missing_values(self, columns: Optional[List[str]] = None, 
                             method: str = 'median') -> pd.DataFrame:
        """
        Impute missing values using specified method.
        
        Parameters:
        -----------
        columns : list of str, optional
            Columns to impute. If None, imputes all numeric columns
        method : str, default 'median'
            Imputation method: 'median', 'mean', or 'mode'
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with imputed values
        """
        if columns is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            columns = list(numeric_cols)
        
        df_imputed = self.df.copy()
        
        for col in columns:
            if col not in df_imputed.columns:
                continue
                
            if method == 'median':
                fill_value = df_imputed[col].median()
            elif method == 'mean':
                fill_value = df_imputed[col].mean()
            elif method == 'mode':
                fill_value = df_imputed[col].mode()[0] if len(df_imputed[col].mode()) > 0 else 0
            else:
                raise ValueError(f"Unknown imputation method: {method}")
            
            df_imputed[col].fillna(fill_value, inplace=True)
        
        self.df = df_imputed
        return df_imputed
    
    def detect_outliers(self, columns: List[str], 
                       z_threshold: float = 3.0) -> pd.DataFrame:
        """
        Detect outliers using Z-score method.
        
        Parameters:
        -----------
        columns : list of str
            Columns to check for outliers
        z_threshold : float, default 3.0
            Z-score threshold for outlier detection
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with outlier flags added
        """
        # Create a copy to avoid modifying original dataframe
        df_with_flags = self.df.copy()
        # Initialize outlier flag column - all rows start as False (no outlier)
        df_with_flags['Outlier_Flag'] = False
        
        for col in columns:
            # Skip if column doesn't exist in dataframe
            if col not in df_with_flags.columns:
                continue
            
            # Calculate Z-scores using scipy.stats (more robust than manual calculation)
            # Z-score = (value - mean) / std_deviation
            # Values with |Z| > threshold are considered outliers
            z_scores = np.abs(stats.zscore(df_with_flags[col].dropna()))
            
            # Create boolean mask: True where |Z-score| > threshold
            # This identifies rows with outliers in the current column
            outlier_mask = np.abs(stats.zscore(df_with_flags[col])) > z_threshold
            
            # Update the Outlier_Flag column: set to True for detected outliers
            # Using .loc ensures we're modifying the dataframe in-place safely
            df_with_flags.loc[outlier_mask, 'Outlier_Flag'] = True
            
            # Store statistics for reporting: count and percentage of outliers
            num_outliers = outlier_mask.sum()
            self.outlier_flags[col] = {
                'count': int(num_outliers),
                'percentage': float((num_outliers / len(df_with_flags)) * 100)
            }
        
        # Update instance dataframe and return
        self.df = df_with_flags
        return df_with_flags
    
    def cap_outliers(self, columns: List[str], 
                    z_threshold: float = 3.0) -> pd.DataFrame:
        """
        Cap outliers to ±z_threshold standard deviations.
        
        This method uses Winsorization: values beyond ±z_threshold standard deviations
        are capped to the boundary values rather than removed.
        
        Parameters:
        -----------
        columns : list of str
            Columns to cap outliers for
        z_threshold : float, default 3.0
            Z-score threshold for capping
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with outliers capped
        """
        # Create copy to avoid modifying original
        df_capped = self.df.copy()
        
        for col in columns:
            # Skip if column doesn't exist
            if col not in df_capped.columns:
                continue
            
            # Calculate mean and standard deviation for the column
            # These are used to determine the capping boundaries
            mean = df_capped[col].mean()
            std = df_capped[col].std()
            
            # Calculate boundaries: values beyond these will be capped
            # Lower bound: mean - (z_threshold * std)
            # Upper bound: mean + (z_threshold * std)
            lower_bound = mean - (z_threshold * std)
            upper_bound = mean + (z_threshold * std)
            
            # Clip values: anything below lower_bound becomes lower_bound,
            # anything above upper_bound becomes upper_bound
            # This preserves the data structure while removing extreme values
            df_capped[col] = df_capped[col].clip(lower=lower_bound, upper=upper_bound)
        
        # Store cleaned dataframe and return
        self.df_cleaned = df_capped
        return df_capped
    
    def clean(self, numeric_columns: Optional[List[str]] = None,
             outlier_columns: Optional[List[str]] = None,
             imputation_method: str = 'median',
             z_threshold: float = 3.0) -> pd.DataFrame:
        """
        Perform complete cleaning pipeline.
        
        Parameters:
        -----------
        numeric_columns : list of str, optional
            Columns to impute missing values for
        outlier_columns : list of str, optional
            Columns to check for outliers
        imputation_method : str, default 'median'
            Method for imputation
        z_threshold : float, default 3.0
            Z-score threshold for outlier detection/capping
            
        Returns:
        --------
        pd.DataFrame
            Cleaned dataframe
        """
        # Detect missing values
        missing_stats = self.detect_missing_values()
        self.cleaning_stats['missing_values'] = missing_stats
        
        # Impute missing values
        if numeric_columns is None:
            numeric_columns = list(self.df.select_dtypes(include=[np.number]).columns)
        
        self.impute_missing_values(columns=numeric_columns, method=imputation_method)
        
        # Detect and cap outliers
        if outlier_columns is None:
            outlier_columns = numeric_columns
        
        self.detect_outliers(columns=outlier_columns, z_threshold=z_threshold)
        self.cap_outliers(columns=outlier_columns, z_threshold=z_threshold)
        
        # Store cleaning statistics
        self.cleaning_stats['outliers'] = self.outlier_flags
        self.cleaning_stats['total_outliers'] = int(self.df['Outlier_Flag'].sum()) if 'Outlier_Flag' in self.df.columns else 0
        
        return self.df_cleaned if self.df_cleaned is not None else self.df
    
    def get_cleaning_report(self) -> dict:
        """
        Get comprehensive cleaning report.
        
        Returns:
        --------
        dict
            Dictionary with cleaning statistics
        """
        return self.cleaning_stats


def clean_solar_data(df: pd.DataFrame,
                    numeric_columns: Optional[List[str]] = None,
                    outlier_columns: Optional[List[str]] = None,
                    imputation_method: str = 'median',
                    z_threshold: float = 3.0) -> Tuple[pd.DataFrame, dict]:
    """
    Convenience function to clean solar data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    numeric_columns : list of str, optional
        Columns to impute missing values for
    outlier_columns : list of str, optional
        Columns to check for outliers
    imputation_method : str, default 'median'
        Method for imputation
    z_threshold : float, default 3.0
        Z-score threshold for outlier detection/capping
        
    Returns:
    --------
    tuple
        (cleaned_dataframe, cleaning_report)
        
    Example:
    --------
    >>> df_clean, report = clean_solar_data(df, 
    ...                                     outlier_columns=['GHI', 'DNI', 'DHI'])
    >>> print(f"Outliers detected: {report['total_outliers']}")
    """
    cleaner = SolarDataCleaner(df)
    df_cleaned = cleaner.clean(
        numeric_columns=numeric_columns,
        outlier_columns=outlier_columns,
        imputation_method=imputation_method,
        z_threshold=z_threshold
    )
    report = cleaner.get_cleaning_report()
    return df_cleaned, report

