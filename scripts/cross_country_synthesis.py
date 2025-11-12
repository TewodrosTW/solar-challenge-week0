"""
Cross-Country Synthesis Script

This script aggregates cleaned datasets from all three countries (Benin, Sierra Leone, Togo)
and performs cross-country analysis and comparison.

This addresses the feedback requirement for a cross-country synthesis script that
aggregates cleaned datasets.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class CrossCountrySynthesizer:
    """
    Class for synthesizing and comparing solar data across multiple countries.
    
    This class aggregates cleaned datasets from multiple countries and provides
    methods for cross-country comparison and analysis.
    """
    
    def __init__(self, data_dir: str = 'data'):
        """
        Initialize the synthesizer.
        
        Parameters:
        -----------
        data_dir : str
            Directory containing cleaned CSV files
        """
        self.data_dir = Path(data_dir)
        self.countries_data: Dict[str, pd.DataFrame] = {}
        self.combined_data: pd.DataFrame = None
        
    def load_country_data(self, country_name: str, file_path: str) -> pd.DataFrame:
        """
        Load cleaned data for a specific country.
        
        Parameters:
        -----------
        country_name : str
            Name of the country (e.g., 'Benin', 'Sierra Leone', 'Togo')
        file_path : str
            Path to the cleaned CSV file
            
        Returns:
        --------
        pd.DataFrame
            Loaded dataframe with country name added
        """
        df = pd.read_csv(file_path)
        
        # Add country identifier column
        df['Country'] = country_name
        
        # Convert Timestamp if it exists
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Store in dictionary
        self.countries_data[country_name] = df
        
        return df
    
    def aggregate_all_countries(self, 
                               file_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Aggregate cleaned datasets from all countries.
        
        Parameters:
        -----------
        file_mapping : dict
            Dictionary mapping country names to file paths
            Example: {'Benin': 'data/benin_clean.csv', ...}
            
        Returns:
        --------
        pd.DataFrame
            Combined dataframe with all countries
        """
        dataframes = []
        
        for country, file_path in file_mapping.items():
            df = self.load_country_data(country, file_path)
            dataframes.append(df)
        
        # Combine all dataframes
        self.combined_data = pd.concat(dataframes, ignore_index=True)
        
        return self.combined_data
    
    def get_summary_statistics(self, 
                              columns: List[str] = ['GHI', 'DNI', 'DHI']) -> pd.DataFrame:
        """
        Generate summary statistics by country.
        
        Parameters:
        -----------
        columns : list of str
            Columns to summarize
            
        Returns:
        --------
        pd.DataFrame
            Summary statistics table with mean, median, std dev for each country
        """
        if self.combined_data is None:
            raise ValueError("No data loaded. Call aggregate_all_countries() first.")
        
        summary_stats = []
        
        for country in self.combined_data['Country'].unique():
            country_df = self.combined_data[self.combined_data['Country'] == country]
            
            stats = {'Country': country}
            for col in columns:
                if col in country_df.columns:
                    stats[f'{col}_mean'] = country_df[col].mean()
                    stats[f'{col}_median'] = country_df[col].median()
                    stats[f'{col}_std'] = country_df[col].std()
                    stats[f'{col}_min'] = country_df[col].min()
                    stats[f'{col}_max'] = country_df[col].max()
            
            summary_stats.append(stats)
        
        return pd.DataFrame(summary_stats)
    
    def create_comparison_boxplots(self, 
                                   columns: List[str] = ['GHI', 'DNI', 'DHI'],
                                   figsize: Tuple[int, int] = (15, 5)) -> None:
        """
        Create side-by-side boxplots comparing countries.
        
        Parameters:
        -----------
        columns : list of str
            Columns to plot
        figsize : tuple
            Figure size (width, height)
        """
        if self.combined_data is None:
            raise ValueError("No data loaded. Call aggregate_all_countries() first.")
        
        n_cols = len(columns)
        fig, axes = plt.subplots(1, n_cols, figsize=figsize)
        
        if n_cols == 1:
            axes = [axes]
        
        for idx, col in enumerate(columns):
            if col not in self.combined_data.columns:
                continue
            
            # Create boxplot with country as hue
            sns.boxplot(data=self.combined_data, 
                       x='Country', 
                       y=col, 
                       ax=axes[idx])
            axes[idx].set_title(f'{col} Distribution by Country')
            axes[idx].set_xlabel('Country')
            axes[idx].set_ylabel(col)
            axes[idx].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('notebooks/cross_country_comparison_boxplots.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def export_combined_data(self, output_path: str = 'data/all_countries_combined.csv') -> Path:
        """
        Export combined dataset to CSV.
        
        Parameters:
        -----------
        output_path : str
            Path where to save the combined CSV
            
        Returns:
        --------
        Path
            Path to exported file
        """
        if self.combined_data is None:
            raise ValueError("No data loaded. Call aggregate_all_countries() first.")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.combined_data.to_csv(output_path, index=False)
        
        return output_path


def synthesize_countries(data_dir: str = 'data',
                         output_path: str = 'data/all_countries_combined.csv') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convenience function to synthesize all country data.
    
    Parameters:
    -----------
    data_dir : str
        Directory containing cleaned CSV files
    output_path : str
        Path where to save combined dataset
        
    Returns:
    --------
    tuple
        (combined_dataframe, summary_statistics_dataframe)
        
    Example:
    --------
    >>> combined_df, summary_df = synthesize_countries()
    >>> print(summary_df)
    """
    synthesizer = CrossCountrySynthesizer(data_dir)
    
    # Define file mapping
    file_mapping = {
        'Benin': f'{data_dir}/benin_clean.csv',
        'Sierra Leone': f'{data_dir}/sierra_leone_clean.csv',
        'Togo': f'{data_dir}/togo_clean.csv'
    }
    
    # Aggregate all countries
    combined_df = synthesizer.aggregate_all_countries(file_mapping)
    
    # Generate summary statistics
    summary_df = synthesizer.get_summary_statistics()
    
    # Export combined data
    synthesizer.export_combined_data(output_path)
    
    # Create comparison visualizations
    synthesizer.create_comparison_boxplots()
    
    return combined_df, summary_df


if __name__ == '__main__':
    """
    Main execution: Run cross-country synthesis.
    
    This script:
    1. Loads cleaned datasets from all three countries
    2. Combines them into a single dataframe
    3. Generates summary statistics
    4. Creates comparison visualizations
    5. Exports combined dataset
    """
    print("=" * 80)
    print("Cross-Country Synthesis")
    print("=" * 80)
    
    # Run synthesis
    combined_df, summary_df = synthesize_countries()
    
    print(f"\nCombined dataset shape: {combined_df.shape}")
    print(f"\nSummary Statistics by Country:")
    print(summary_df)
    
    print(f"\nCombined data exported to: data/all_countries_combined.csv")
    print("\nVisualizations saved to: notebooks/cross_country_comparison_boxplots.png")

