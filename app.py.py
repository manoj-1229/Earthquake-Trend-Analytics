import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Earthquake Trend Analytics",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def generate_and_load_data():
    filename = "usgs_earthquake_trends_dataset.csv"
    if not os.path.exists(filename):
        np.random.seed(42)
        num_records = 5000
        start_date = pd.to_datetime('1970-01-01')
        end_date = pd.to_datetime('2025-12-31')
        random_dates = start_date + (end_date - start_date) * np.random.rand(num_records)
        magnitudes = 3.0 + np.random.exponential(scale=1.1, size=num_records)
        magnitudes = np.clip(magnitudes, 3.0, 9.2)
        
        depth_choices = (
            [np.random.uniform(0, 70) for _ in range(int(num_records * 0.75))] +
            [np.random.uniform(70, 300) for _ in range(int(num_records * 0.20))] +
            [np.random.uniform(300, 700) for _ in range(int(num_records * 0.05))]
        )
        np.random.shuffle(depth_choices)
        depths = np.array(depth_choices)[:num_records]
        
        regions = [
            'Ring of Fire - Alaska', 'Ring of Fire - Japan', 'Ring of Fire - Chile', 
            'Ring of Fire - Indonesia', 'Ring of Fire - California', 'Mid-Atlantic Ridge', 
            'Mediterranean-Hayan Belt', 'Ring of Fire - Philippines', 'Ring of Fire - New Zealand',
            'Hawaii Volcanic Region', 'Stable Continental Region'
        ]
        region_probs = [0.25, 0.20, 0.15, 0.12, 0.10, 0.05, 0.06, 0.03, 0.02, 0.01, 0.01]
        location_labels = np.random.choice(regions, size=num_records, p=region_probs)
        
        df_raw = pd.DataFrame({
            'time': random_dates,
            'latitude': np.random.uniform(-90, 90, size=num_records),
            'longitude': np.random.uniform(-180, 180, size=num_records),
            'depth': depths,
            'mag': magnitudes,
            'place': location_labels,
            'status': 'reviewed'
        })
        df_raw['year'] = df_raw['time'].dt.year
        mask = (df_raw['year'] < 2000) & (np.random.rand(num_records) > 0.4)
        df_raw = df_raw[~mask].reset_index(drop=True)
        df_raw = df_raw.drop(columns=['year'], errors='ignore')
        df_raw.to_csv(filename, index=False)
    
    df = pd.read_csv(filename)
    df['time'] = pd.to_datetime(df['time'])
    df = df.dropna(subset=['latitude', 'longitude', 'mag', 'depth'])
    df = df[df['mag'] >= 3.0]
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    return df

df = generate_and_load_data()

st.title("🌋 Earthquake Trend Analytics Dashboard")
st.markdown("### Analyzing Long-Term Global Seismic Trends (1970–2025)")

st.sidebar.header("Filter Seismic Catalog")
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['year'].min()),
    int(df['year'].max()),
    (1970, 2025)
)
mag_range = st.sidebar.slider(
    "Select Magnitude Range (Richter)",
    float(df['mag'].min()),
    float(df['mag'].max()),
    (3.0, 9.5),
    step=0.1
)

filtered_df = df[
    (df['year'] >= year_range[0]) & (df['year'] <= year_range[1]) &
    (df['mag'] >= mag_range[0]) & (df['mag'] <= mag_range[1])
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Recorded Events", len(filtered_df))
col2.metric("Max Magnitude", f"{filtered_df['mag'].max():.1f} Mw")
col3.metric("Average Magnitude", f"{filtered_df['mag'].mean():.2f} Mw")
col4.metric("Average Depth", f"{filtered_df['depth'].mean():.1f} km")

st.markdown("---")

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'axes.labelsize': 11, 'axes.titlesize': 13,
    'xtick.labelsize': 9, 'ytick.labelsize': 9
})

tab1, tab2, tab3 = st.tabs(["📊 Temporal & Regional Trends", "📈 Geological Distributions", "🗺️ Interactive Geospatial Mapping"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Yearly Frequency Trends")
        fig, ax = plt.subplots(figsize=(10, 5))
        yearly = filtered_df.groupby('year').size()
        sns.lineplot(x=yearly.index, y=yearly.values, marker='o', color='#1e3a8a', linewidth=2.5, ax=ax)
        ax.set_xlabel("Calendar Years")
        ax.set_ylabel("Event Count")
        st.pyplot(fig)
    with c2:
        st.subheader("Monthly Seasonal Control-Test")
        fig, ax = plt.subplots(figsize=(10, 5))
        monthly = filtered_df.groupby('month').size()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        sns.barplot(x=month_names, y=monthly.values, color='#0284c7', edgecolor='#0f172a', ax=ax)
        ax.set_xlabel("Months")
        ax.set_ylabel("Aggregated Event Count")
        st.pyplot(fig)

    st.subheader("Top 10 High-Frequency Seismic Regions")
    fig, ax = plt.subplots(figsize=(12, 5))
    top_regions = filtered_df['place'].value_counts().head(10)
    sns.barplot(x=top_regions.values, y=top_regions.index, palette='flare', edgecolor='#0f172a', ax=ax)
    ax.set_xlabel("Confirmed Incident Records")
    ax.set_ylabel("Tectonic Subzones")
    st.pyplot(fig)

with tab2:
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Magnitude Frequency Profile")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(filtered_df['mag'], bins=25, kde=True, color='#dc2626', edgecolor='white', alpha=0.75, ax=ax)
        ax.axvline(filtered_df['mag'].mean(), color='#1e3a8a', linestyle='--', linewidth=2, label=f"Mean M: {filtered_df['mag'].mean():.2f}")
        ax.set_xlabel("Magnitude Scale Value (M)")
        ax.set_ylabel("Occurrence Density")
        ax.legend()
        st.pyplot(fig)
    with c4:
        st.subheader("Depth vs. Magnitude Correlation Profile")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(data=filtered_df, x='mag', y='depth', alpha=0.4, color='#84cc16', edgecolor='none', ax=ax)
        ax.set_xlabel("Magnitude (M)")
        ax.set_ylabel("Hypocentral Depth (km)")
        ax.invert_yaxis()
        st.pyplot(fig)

    st.subheader("Pairwise Variable Correlation Matrix")
    fig, ax = plt.subplots(figsize=(8, 4))
    features = ['mag', 'depth', 'latitude', 'longitude', 'year', 'month']
    sns.heatmap(filtered_df[features].corr(), annot=True, cmap='coolwarm', fmt=".4f", linewidths=0.5, square=True, ax=ax)
    st.pyplot(fig)

with tab3:
    st.subheader("Geospatial Distribution of Filtered Seismic Events")
    map_data = filtered_df[['latitude', 'longitude', 'mag', 'depth']].rename(columns={'latitude': 'lat', 'longitude': 'lon'})
    
    
    map_data['scaled_marker_size'] = map_data['mag'] * 10 
    st.map(map_data, size='scaled_marker_size', color='#dc2626')

st.markdown("---")
st.dataframe(filtered_df[['time', 'place', 'mag', 'depth', 'latitude', 'longitude']].sort_values('time', ascending=False).head(100), use_container_width=True)
