"""
Data Export Module

This module provides reusable functions for exporting cleaned datasets.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional, Union


class SolarDataExporter:
    """
    A class for exporting cleaned solar data.
    
    This class handles:
    - Exporting to CSV
    - Removing temporary columns
    - Data validation before export
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the data exporter.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Dataframe to export
        """
        self.df = df.copy()
        
    def remove_temp_columns(self, temp_columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove temporary columns used during analysis.
        
        Parameters:
        -----------
        temp_columns : list of str, optional
            List of temporary columns to remove.
            Default: ['Hour', 'Month', 'Day', 'WD_bin', 'Outlier_Flag']
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with temporary columns removed
        """
        if temp_columns is None:
            temp_columns = ['Hour', 'Month', 'Day', 'WD_bin', 'Outlier_Flag']
        
        columns_to_remove = [col for col in temp_columns if col in self.df.columns]
        self.df = self.df.drop(columns=columns_to_remove)
        
        return self.df
    
    def export(self, output_path: Union[str, Path],
              remove_temp: bool = True,
              temp_columns: Optional[List[str]] = None,
              index: bool = False) -> Path:
        """
        Export cleaned dataframe to CSV.
        
        Parameters:
        -----------
        output_path : str or Path
            Path where to save the cleaned CSV file
        remove_temp : bool, default True
            Whether to remove temporary columns before export
        temp_columns : list of str, optional
            Temporary columns to remove (if remove_temp=True)
        index : bool, default False
            Whether to include index in export
            
        Returns:
        --------
        Path
            Path to the exported file
            
        Example:
        --------
        >>> exporter = SolarDataExporter(df_cleaned)
        >>> output_file = exporter.export('data/benin_clean.csv')
        >>> print(f"Exported to: {output_file}")
        """
        output_path = Path(output_path)
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove temporary columns if requested
        if remove_temp:
            self.remove_temp_columns(temp_columns)
        
        # Export to CSV
        self.df.to_csv(output_path, index=index)
        
        return output_path


def export_cleaned_data(df: pd.DataFrame,
                        output_path: Union[str, Path],
                        remove_temp: bool = True,
                        temp_columns: Optional[List[str]] = None,
                        index: bool = False) -> Path:
    """
    Convenience function to export cleaned data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned dataframe to export
    output_path : str or Path
        Path where to save the cleaned CSV file
    remove_temp : bool, default True
        Whether to remove temporary columns before export
    temp_columns : list of str, optional
        Temporary columns to remove (if remove_temp=True)
    index : bool, default False
        Whether to include index in export
        
    Returns:
    --------
    Path
        Path to the exported file
        
    Example:
    --------
    >>> output_file = export_cleaned_data(df_cleaned, 'data/benin_clean.csv')
    >>> print(f"Exported to: {output_file}")
    """
    exporter = SolarDataExporter(df)
    return exporter.export(
        output_path=output_path,
        remove_temp=remove_temp,
        temp_columns=temp_columns,
        index=index
    )

