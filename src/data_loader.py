"""
Data Loading Module

This module provides reusable functions for loading and preprocessing solar data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Union


class SolarDataLoader:
    """
    A class for loading and preprocessing solar irradiance data.
    
    This class handles:
    - Loading CSV files
    - Converting timestamps
    - Basic data validation
    - Setting up time series index
    """
    
    def __init__(self, data_path: Union[str, Path]):
        """
        Initialize the data loader.
        
        Parameters:
        -----------
        data_path : str or Path
            Path to the CSV data file
        """
        self.data_path = Path(data_path)
        self.df = None
        self.df_indexed = None
        
    def load(self, timestamp_col: str = 'Timestamp') -> pd.DataFrame:
        """
        Load the dataset from CSV file.
        
        Parameters:
        -----------
        timestamp_col : str, default 'Timestamp'
            Name of the timestamp column
            
        Returns:
        --------
        pd.DataFrame
            Loaded dataframe with timestamp converted to datetime
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        self.df = pd.read_csv(self.data_path)
        
        # Convert timestamp to datetime
        if timestamp_col in self.df.columns:
            self.df[timestamp_col] = pd.to_datetime(self.df[timestamp_col])
        else:
            raise ValueError(f"Timestamp column '{timestamp_col}' not found in data")
        
        return self.df
    
    def set_time_index(self, timestamp_col: str = 'Timestamp') -> pd.DataFrame:
        """
        Set timestamp as index for time series analysis.
        
        Parameters:
        -----------
        timestamp_col : str, default 'Timestamp'
            Name of the timestamp column
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with timestamp as index
        """
        if self.df is None:
            raise ValueError("Data must be loaded first. Call load() method.")
        
        self.df_indexed = self.df.set_index(timestamp_col)
        return self.df_indexed
    
    def get_info(self) -> dict:
        """
        Get basic information about the dataset.
        
        Returns:
        --------
        dict
            Dictionary containing dataset information
        """
        if self.df is None:
            raise ValueError("Data must be loaded first. Call load() method.")
        
        info = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'numeric_columns': list(self.df.select_dtypes(include=[np.number]).columns),
            'date_range': (
                self.df['Timestamp'].min(),
                self.df['Timestamp'].max()
            ) if 'Timestamp' in self.df.columns else None,
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }
        
        return info


def load_solar_data(file_path: Union[str, Path], 
                   timestamp_col: str = 'Timestamp') -> pd.DataFrame:
    """
    Convenience function to load solar data.
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the CSV data file
    timestamp_col : str, default 'Timestamp'
        Name of the timestamp column
        
    Returns:
    --------
    pd.DataFrame
        Loaded dataframe with timestamp converted to datetime
        
    Example:
    --------
    >>> df = load_solar_data('data/benin-malanville.csv')
    >>> print(df.shape)
    (525600, 19)
    """
    loader = SolarDataLoader(file_path)
    df = loader.load(timestamp_col)
    return df

