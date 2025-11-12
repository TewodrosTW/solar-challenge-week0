"""
Unit tests for data_cleaner module
"""

import pytest
import pandas as pd
import numpy as np
from src.data_cleaner import SolarDataCleaner, clean_solar_data


class TestSolarDataCleaner:
    """Test cases for SolarDataCleaner class"""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample dataframe for testing"""
        np.random.seed(42)
        df = pd.DataFrame({
            'GHI': np.random.normal(240, 50, 1000),
            'DNI': np.random.normal(167, 40, 1000),
            'DHI': np.random.normal(115, 30, 1000),
            'Tamb': np.random.normal(28, 3, 1000)
        })
        # Add some missing values
        df.loc[0:10, 'GHI'] = np.nan
        # Add some outliers
        df.loc[100:105, 'DNI'] = 1000
        return df
    
    def test_cleaner_initialization(self, sample_df):
        """Test cleaner initialization"""
        cleaner = SolarDataCleaner(sample_df)
        assert cleaner.df is not None
        assert len(cleaner.df) == 1000
    
    def test_detect_missing_values(self, sample_df):
        """Test missing value detection"""
        cleaner = SolarDataCleaner(sample_df)
        missing_stats = cleaner.detect_missing_values()
        
        assert 'total_missing' in missing_stats
        assert 'missing_by_column' in missing_stats
        assert missing_stats['total_missing'] > 0
    
    def test_impute_missing_values(self, sample_df):
        """Test missing value imputation"""
        cleaner = SolarDataCleaner(sample_df)
        df_imputed = cleaner.impute_missing_values(columns=['GHI'], method='median')
        
        assert df_imputed['GHI'].isna().sum() == 0
    
    def test_detect_outliers(self, sample_df):
        """Test outlier detection"""
        cleaner = SolarDataCleaner(sample_df)
        cleaner.impute_missing_values()  # First impute missing values
        df_with_flags = cleaner.detect_outliers(['DNI'], z_threshold=3.0)
        
        assert 'Outlier_Flag' in df_with_flags.columns
        assert df_with_flags['Outlier_Flag'].sum() > 0  # Should detect outliers
    
    def test_cap_outliers(self, sample_df):
        """Test outlier capping"""
        cleaner = SolarDataCleaner(sample_df)
        cleaner.impute_missing_values()
        cleaner.detect_outliers(['DNI'])
        df_capped = cleaner.cap_outliers(['DNI'], z_threshold=3.0)
        
        # Check that outliers are capped
        mean = df_capped['DNI'].mean()
        std = df_capped['DNI'].std()
        max_value = df_capped['DNI'].max()
        min_value = df_capped['DNI'].min()
        
        assert max_value <= mean + 3 * std
        assert min_value >= mean - 3 * std
    
    def test_complete_clean_pipeline(self, sample_df):
        """Test complete cleaning pipeline"""
        cleaner = SolarDataCleaner(sample_df)
        df_cleaned = cleaner.clean(
            numeric_columns=['GHI', 'DNI', 'DHI', 'Tamb'],
            outlier_columns=['GHI', 'DNI'],
            z_threshold=3.0
        )
        
        assert df_cleaned is not None
        assert df_cleaned['GHI'].isna().sum() == 0
        assert 'Outlier_Flag' in df_cleaned.columns or cleaner.df_cleaned is not None


class TestCleanSolarDataFunction:
    """Test cases for clean_solar_data convenience function"""
    
    def test_clean_solar_data_function(self):
        """Test convenience function"""
        np.random.seed(42)
        df = pd.DataFrame({
            'GHI': np.random.normal(240, 50, 100),
            'DNI': np.random.normal(167, 40, 100)
        })
        df.loc[0:5, 'GHI'] = np.nan
        
        df_cleaned, report = clean_solar_data(
            df,
            numeric_columns=['GHI', 'DNI'],
            outlier_columns=['GHI', 'DNI']
        )
        
        assert df_cleaned is not None
        assert 'missing_values' in report
        assert 'outliers' in report

