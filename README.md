# Solar Challenge Week 0 - West Africa Solar Data Analysis

**Repository:** [https://github.com/Danielmituku/solar-challenge-week0](https://github.com/Danielmituku/solar-challenge-week0)

This repository contains a comprehensive analysis of solar irradiance data from three West African countries (Benin, Sierra Leone, and Togo), including exploratory data analysis, statistical comparisons, and an interactive Streamlit dashboard.

## Setup Environment

Follow these steps to reproduce the development environment:

### Prerequisites

- **Python 3.13** (or compatible version)
- **pip** (Python package installer)
- **Git** (for version control)

### Installation Steps

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/Danielmituku/solar-challenge-week0.git
   cd solar-challenge-week0
   ```

2. **Create a virtual environment**:
   
   On Windows:
   ```bash
   python -m venv venv
   ```
   
   On macOS/Linux:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   
   On Windows (PowerShell):
   ```bash
   .\venv\Scripts\Activate.ps1
   ```
   
   On Windows (Command Prompt):
   ```bash
   venv\Scripts\activate.bat
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify the installation**:
   ```bash
   python --version
   pip list
   ```

### Project Structure

```
solar-challenge-week0/
├── app/               # Streamlit dashboard application
│   ├── __init__.py
│   ├── main.py        # Main dashboard script
│   └── utils.py       # Dashboard utilities
├── data/              # Data files (gitignored)
├── notebooks/         # Jupyter notebooks
├── scripts/           # Utility scripts
├── src/               # Source code modules
├── tests/             # Test files
├── venv/              # Virtual environment (gitignored)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

### Running Tests

To run tests using pytest:
```bash
pytest tests/
```

### Notes

- The virtual environment (`venv/`) is excluded from version control (see `.gitignore`)
- Make sure to activate the virtual environment before working on the project
- If you encounter any issues, ensure you're using Python 3.13 or a compatible version

## Project Deliverables

### Main Branch Links

All deliverables are available on the main branch:

- **📊 EDA Notebooks:** See `notebooks/` directory
  - `benin_eda.ipynb` - Benin exploratory data analysis
  - `sierra_leone_eda.ipynb` - Sierra Leone exploratory data analysis
  - `togo_eda.ipynb` - Togo exploratory data analysis

- **📁 Cleaned Datasets:** See `data/` directory
  - `benin_clean.csv` - Cleaned Benin dataset
  - `sierra_leone_clean.csv` - Cleaned Sierra Leone dataset
  - `togo_clean.csv` - Cleaned Togo dataset

- **🔧 Reusable Modules:** See `src/` directory
  - `data_loader.py` - Data loading functionality
  - `data_cleaner.py` - Data cleaning functionality
  - `data_exporter.py` - Data export functionality
  - See `src/README.md` for module documentation

- **📊 Cross-Country Comparison:** See `notebooks/` directory
  - `compare_countries.ipynb` - Statistical comparison across countries

- **🌐 Interactive Dashboard:** See `app/` directory
  - `app/main.py` - Streamlit dashboard application
  - `app/utils.py` - Dashboard utility functions
  - Run with: `streamlit run app/main.py`


## Using Reusable Modules

Instead of procedural code in notebooks, you can use the modular functions:

```python
from src import load_solar_data, clean_solar_data, export_cleaned_data

# Load data
df = load_solar_data('data/benin-malanville.csv')

# Clean data
df_cleaned, report = clean_solar_data(
    df,
    outlier_columns=['GHI', 'DNI', 'DHI'],
    z_threshold=3.0
)

# Export cleaned data
export_cleaned_data(df_cleaned, 'data/benin_clean.csv')
```

See `scripts/example_usage.py` for more examples.

## Streamlit Dashboard

### Running Locally

1. **Activate virtual environment:**
   ```bash
   .\venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate      # Mac/Linux
   ```

2. **Run the dashboard:**
   ```bash
   streamlit run app/main.py
   ```

3. **Open browser to http://localhost:8501**

### Features

- **Country Selection**: Multi-select widget to choose countries (Benin, Sierra Leone, Togo)
- **Date Range Filter**: Filter data by date range in the sidebar
- **GHI Boxplot**: Interactive visualization of Global Horizontal Irradiance distribution
- **DNI Boxplot**: Direct Normal Irradiance distribution visualization
- **DHI Boxplot**: Diffuse Horizontal Irradiance distribution visualization
- **Time Series Plot**: Daily average GHI over time with country comparison
- **Top Regions Table**: Summary statistics by country (mean, median, std dev for GHI, DNI, DHI)
- **Real-time Filtering**: All visualizations update automatically based on selections
- **Performance Optimized**: Cached data loading and efficient filtering operations

### Dashboard Structure

```
app/
├── __init__.py
├── main.py          # Main Streamlit application
└── utils.py         # Utility functions for data processing
```

### Deployment

The dashboard can be deployed to Streamlit Community Cloud:
Or already deployed with the link:  https://dashboard-solar-challenge-week0.streamlit.app/

1. **Push code to GitHub** (ensure `app/main.py` exists)
2. **Connect repository to Streamlit Cloud**:
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
3. **Configure deployment**:
   - Select repository: `solar-challenge-week0`
   - Set main file path: `app/main.py`
   - Select branch: `dashboard-dev` or `main`
4. **Deploy** and access via public URL

### Requirements

The dashboard requires the following packages (already in `requirements.txt`):
- `streamlit>=1.45.0`
- `pandas>=2.3.3`
- `plotly>=6.4.0`
- `numpy>=2.3.4`

## Documentation

- **[Source Code Modules](src/README.md)** - Detailed module documentation with usage examples
- **[Commit Message Guide](docs/COMMIT_MESSAGE_GUIDE.md)** - Best practices for commit messages
- **[Streamlit Dashboard](docs/STREAMLIT_DASHBOARD.md)** - Planned dashboard interface documentation
- **[Cross-Country Synthesis](scripts/cross_country_synthesis.py)** - Script for aggregating country data
- **[Bonus Dashboard Guide](BONUS_DASHBOARD_STEP_BY_STEP_GUIDE.md)** - Step-by-step guide for dashboard development
