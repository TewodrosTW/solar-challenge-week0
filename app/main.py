import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.utils import (
    load_all_countries_data,
    load_data_from_uploaded_files,
    filter_data_by_countries,
    create_summary_table
)

# Page configuration
st.set_page_config(
    page_title="Solar Data Dashboard - West Africa",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("☀️ Solar Irradiance Dashboard - West Africa")
st.markdown("Interactive visualization of solar potential across Benin, Sierra Leone, and Togo")

# Sidebar - File Upload Section
st.sidebar.header("📁 Data Source")

# Option to choose data source
data_source = st.sidebar.radio(
    "Choose data source:",
    ["Upload Files", "Use Local Files"],
    help="Upload CSV files or use files from local directory"
)

df = None

if data_source == "Upload Files":
    st.sidebar.subheader("📤 Upload Cleaned CSV Files")
    
    st.sidebar.info(
        """
        **Upload your cleaned CSV files:**
        - Files should have a `Timestamp` column
        - Must include `GHI`, `DNI`, `DHI` columns
        - You can upload 1-3 files (at least one required)
        """
    )
    
    uploaded_benin = st.sidebar.file_uploader(
        "Upload Benin Cleaned CSV",
        type=['csv'],
        key='benin',
        help="Upload benin_clean.csv file"
    )
    
    uploaded_sierra_leone = st.sidebar.file_uploader(
        "Upload Sierra Leone Cleaned CSV",
        type=['csv'],
        key='sierra_leone',
        help="Upload sierra_leone_clean.csv file"
    )
    
    uploaded_togo = st.sidebar.file_uploader(
        "Upload Togo Cleaned CSV",
        type=['csv'],
        key='togo',
        help="Upload togo_clean.csv file"
    )
    
    # Check if at least one file is uploaded
    uploaded_files = {
        'benin': uploaded_benin,
        'sierra_leone': uploaded_sierra_leone,
        'togo': uploaded_togo
    }
    
    if any(uploaded_files.values()):
        try:
            with st.spinner("Loading uploaded data..."):
                from app.utils import load_data_from_uploaded_files
                df = load_data_from_uploaded_files(uploaded_files)
                st.sidebar.success(f"✅ Loaded {len(df):,} records")
        except Exception as e:
            st.error(f"❌ Error loading uploaded files: {str(e)}")
            st.stop()
    else:
        st.info("👆 Please upload at least one cleaned CSV file to get started.")
        st.stop()

else:  # Use Local Files
    # Load data with caching
    @st.cache_data
    def load_data():
        """Load and cache the combined dataset."""
        return load_all_countries_data()
    
    # Load data (cached)
    try:
        df = load_data()
        st.sidebar.success(f"✅ Loaded {len(df):,} records from local files")
    except FileNotFoundError as e:
        st.error(f"❌ Data Loading Error: {str(e)}")
        st.info(
            """
            **Local files not found.**
            
            Please switch to "Upload Files" mode in the sidebar to upload your CSV files,
            or ensure the cleaned CSV files are in the `data/` directory.
            
            **Files needed:**
            - `data/benin_clean.csv`
            - `data/sierra_leone_clean.csv`
            - `data/togo_clean.csv`
            """
        )
        st.stop()

if df is None or len(df) == 0:
    st.warning("⚠️ No data available. Please upload files or check local file paths.")
    st.stop()

# Pre-compute date range for better performance
# Recalculate if data changes (for uploaded files)
if 'df_hash' not in st.session_state or st.session_state.df_hash != hash(str(df.shape) + str(df['Timestamp'].min()) + str(df['Timestamp'].max())):
    st.session_state.min_date = df['Timestamp'].min().date()
    st.session_state.max_date = df['Timestamp'].max().date()
    st.session_state.df_hash = hash(str(df.shape) + str(df['Timestamp'].min()) + str(df['Timestamp'].max()))

min_date = st.session_state.min_date
max_date = st.session_state.max_date

# Sidebar
st.sidebar.header("📊 Filters")

# Get available countries from loaded data
available_countries = sorted(df['Country'].unique().tolist()) if df is not None and len(df) > 0 else []

# Country selection widget
if available_countries:
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=available_countries,
        default=available_countries,
        help="Choose one or more countries to visualize"
    )
else:
    selected_countries = []

# Date range filter
st.sidebar.subheader("📅 Date Range")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Filter data by date range"
)

# Filter data by countries first (more efficient)
if selected_countries:
    filtered_df = filter_data_by_countries(df, selected_countries)
else:
    st.warning("⚠️ Please select at least one country")
    st.stop()
    filtered_df = df

# Filter by date range if both dates selected (optimize with datetime comparison)
if len(date_range) == 2:
    start_date, end_date = date_range
    # Convert to datetime for faster comparison
    start_datetime = pd.Timestamp(start_date)
    end_datetime = pd.Timestamp(end_date) + pd.Timedelta(days=1)  # Include end date
    filtered_df = filtered_df[
        (filtered_df['Timestamp'] >= start_datetime) &
        (filtered_df['Timestamp'] < end_datetime)
    ]

# Main content area - Quick Stats
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", f"{len(filtered_df):,}")
with col2:
    st.metric("Countries Selected", len(selected_countries))
with col3:
    st.metric("Date Range", 
              f"{filtered_df['Timestamp'].min().date()} to {filtered_df['Timestamp'].max().date()}")

# Tabs for different metrics
tab1, tab2, tab3, tab4 = st.tabs(["📊 GHI", "📊 DNI", "📊 DHI", "📈 Time Series"])

# Color mapping
color_map = {
    'Benin': '#2ecc71',
    'Sierra Leone': '#3498db',
    'Togo': '#e74c3c'
}

# Helper function to create boxplot (cached for performance)
@st.cache_data
def create_boxplot_cached(df, metric, title, y_label, color_map):
    """Create a boxplot for the given metric (cached)."""
    fig = px.box(
        df,
        x='Country',
        y=metric,
        color='Country',
        title=title,
        labels={metric: y_label, 'Country': 'Country'},
        color_discrete_map=color_map
    )
    fig.update_layout(
        showlegend=False,
        height=500,
        xaxis_title="Country",
        yaxis_title=y_label
    )
    return fig

# Non-cached version for dynamic updates
def create_boxplot(df, metric, title, y_label):
    """Create a boxplot for the given metric."""
    fig = px.box(
        df,
        x='Country',
        y=metric,
        color='Country',
        title=title,
        labels={metric: y_label, 'Country': 'Country'},
        color_discrete_map=color_map
    )
    fig.update_layout(
        showlegend=False,
        height=500,
        xaxis_title="Country",
        yaxis_title=y_label
    )
    return fig

# Tab 1: GHI Boxplot
with tab1:
    st.header("📈 Global Horizontal Irradiance (GHI) Distribution")
    fig_ghi = create_boxplot(
        filtered_df,
        'GHI',
        'Global Horizontal Irradiance (GHI) Distribution',
        'GHI (W/m²)'
    )
    st.plotly_chart(fig_ghi, use_container_width=True)

# Tab 2: DNI Boxplot
with tab2:
    st.header("📈 Direct Normal Irradiance (DNI) Distribution")
    fig_dni = create_boxplot(
        filtered_df,
        'DNI',
        'Direct Normal Irradiance (DNI) Distribution',
        'DNI (W/m²)'
    )
    st.plotly_chart(fig_dni, use_container_width=True)

# Tab 3: DHI Boxplot
with tab3:
    st.header("📈 Diffuse Horizontal Irradiance (DHI) Distribution")
    fig_dhi = create_boxplot(
        filtered_df,
        'DHI',
        'Diffuse Horizontal Irradiance (DHI) Distribution',
        'DHI (W/m²)'
    )
    st.plotly_chart(fig_dhi, use_container_width=True)

# Tab 4: Time Series Plot
with tab4:
    st.header("📈 Daily Average GHI Over Time")
    
    # Optimize: Use resample for daily aggregation (much faster)
    if len(filtered_df) > 0:
        # Create a copy to avoid SettingWithCopyWarning
        ts_df = filtered_df[['Timestamp', 'Country', 'GHI']].copy()
        ts_df.set_index('Timestamp', inplace=True)
        
        # Resample to daily and calculate mean (much faster than groupby)
        daily_avg = ts_df.groupby('Country').resample('D')['GHI'].mean().reset_index()
        
        fig_time = px.line(
            daily_avg,
            x='Timestamp',
            y='GHI',
            color='Country',
            title='Daily Average Global Horizontal Irradiance (GHI) Over Time',
            labels={'GHI': 'Average GHI (W/m²)', 'Timestamp': 'Date'},
            color_discrete_map=color_map
        )
        
        fig_time.update_layout(
            height=500,
            xaxis_title="Date",
            yaxis_title="Average GHI (W/m²)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Top Regions Table
st.header("🏆 Top Regions by Average GHI")
summary_table = create_summary_table(filtered_df)

# Display table
st.dataframe(
    summary_table,
    use_container_width=True,
    hide_index=True
)

# Additional information
st.markdown("---")
st.markdown("### 📝 Notes")
st.info(
    """
    - **GHI**: Global Horizontal Irradiance - total solar radiation received
    - **DNI**: Direct Normal Irradiance - direct beam radiation
    - **DHI**: Diffuse Horizontal Irradiance - scattered radiation
    - Data is from cleaned datasets (outliers removed, missing values imputed)
    """
)

