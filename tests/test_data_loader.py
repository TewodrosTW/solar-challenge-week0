"""
Unit tests for data_loader module
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.data_loader import SolarDataLoader, load_solar_data


class TestSolarDataLoader:
    """Test cases for SolarDataLoader class"""
    
    def test_loader_initialization(self, tmp_path):
        """Test loader initialization"""
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({
            'Timestamp': pd.date_range('2021-01-01', periods=10, freq='H'),
            'GHI': np.random.rand(10) * 100,
            'DNI': np.random.rand(10) * 100
        })
        df.to_csv(test_file, index=False)
        
        loader = SolarDataLoader(test_file)
        assert loader.data_path == test_file
        assert loader.df is None
    
    def test_load_data(self, tmp_path):
        """Test loading data from CSV"""
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({
            'Timestamp': pd.date_range('2021-01-01', periods=10, freq='H'),
            'GHI': np.random.rand(10) * 100,
            'DNI': np.random.rand(10) * 100
        })
        df.to_csv(test_file, index=False)
        
        loader = SolarDataLoader(test_file)
        loaded_df = loader.load()
        
        assert loaded_df is not None
        assert len(loaded_df) == 10
        assert pd.api.types.is_datetime64_any_dtype(loaded_df['Timestamp'])
    
    def test_set_time_index(self, tmp_path):
        """Test setting timestamp as index"""
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({
            'Timestamp': pd.date_range('2021-01-01', periods=10, freq='H'),
            'GHI': np.random.rand(10) * 100
        })
        df.to_csv(test_file, index=False)
        
        loader = SolarDataLoader(test_file)
        loader.load()
        indexed_df = loader.set_time_index()
        
        assert indexed_df.index.name == 'Timestamp'
        assert isinstance(indexed_df.index, pd.DatetimeIndex)
    
    def test_get_info(self, tmp_path):
        """Test getting dataset information"""
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({
            'Timestamp': pd.date_range('2021-01-01', periods=10, freq='H'),
            'GHI': np.random.rand(10) * 100,
            'DNI': np.random.rand(10) * 100
        })
        df.to_csv(test_file, index=False)
        
        loader = SolarDataLoader(test_file)
        loader.load()
        info = loader.get_info()
        
        assert 'shape' in info
        assert 'columns' in info
        assert 'numeric_columns' in info
        assert info['shape'] == (10, 3)


class TestLoadSolarDataFunction:
    """Test cases for load_solar_data convenience function"""
    
    def test_load_solar_data_function(self, tmp_path):
        """Test convenience function"""
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({
            'Timestamp': pd.date_range('2021-01-01', periods=5, freq='H'),
            'GHI': np.random.rand(5) * 100
        })
        df.to_csv(test_file, index=False)
        
        loaded_df = load_solar_data(test_file)
        
        assert len(loaded_df) == 5
        assert 'Timestamp' in loaded_df.columns

