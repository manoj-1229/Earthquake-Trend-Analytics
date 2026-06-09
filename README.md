# 🌋 Earthquake Trend Analytics Dashboard

An interactive, production-ready data science application built with **Python**, **Streamlit**, and **Plotly** to visualize, parse, and analyze multi-decade global seismic events from 1970 to 2025. 

Live Link: [https://earthquake-trend-analytics.streamlit.app/](https://earthquake-trend-analytics.streamlit.app/)

---

## 🚀 App Functioning & Features

The platform is structured into three specialized analytical modules to optimize user exploration and eliminate information clutter:

1. **📊 Temporal & Regional Trends:** Displays real-world key performance indicators (KPIs) like Total Events, Max Magnitude, and Average Hypocentral Depth alongside dynamic timeline line-charts tracking seismic frequencies over years and months.
2. **📈 Geological Distributions:** Employs Seaborn and Matplotlib to map non-linear variables, including depth-versus-magnitude scatter plots and variable correlation heatmaps to extract geodynamic relationships.
3. **🗺️ Interactive Geospatial Mapping:** Generates a clean, bounded world map tracking exact coordinate distributions without continent distortion or wrap-around duplication.

---

## 🛠️ Data Pipeline & Attributes

The dashboard parses real historical coordinates sourced from the **United States Geological Survey (USGS)** database. Every row captures specific geodynamic markers:
* **`time` / `year` / `month`:** Precise chronological markers mapping event frequency cycles.
* **`latitude` / `longitude`:** Exact geographical coordinate points charting fault line borders.
* **`mag` (Magnitude):** Richter/Moment scale representation of energy released.
* **`depth`:** Hypocentral depth measured in kilometers ($km$) beneath the earth's crust surface layer.

---

## 📐 Technical Spotlight: Ground-Distance Map Scaling

A key engineering implementation in this project is the **Geospatial Marker Scale Engine**. 

### The Scaling Problem
Standard mapping modules interpret coordinate radius sizes in **literal ground meters** rather than static display screen pixels. In earlier iterations, multiplying a raw Richter magnitude (e.g., $9.2\text{ Mw}$) by an inflated scale modifier ($15,000$) forced the visualization engine to calculate a radius footprint of over **138,000 meters ($138\text{ km}$)** for a single epicenter:

$$\text{Radius Size Parameter} = \text{Magnitude Value} \times \text{Scale Factor}$$

$$9.2 \times 15,000 = 138,000\text{ meters} \implies 138\text{ km}$$

When thousands of recorded events were plotted simultaneously across tight geographic zones, these massive hundred-kilometer circle boundaries overlapped extensively, causing global continent distortion and creating an unreadable solid red hourglass shape across the viewport.

### The Bounded Optimization Fix
To correct this and optimize user readability, the architecture was refactored to drop base-map wrapping and deploy a bounded **Plotly mapping engine (`px.scatter_map`)**. The scale multiplier was calibrated down to a tight factor of $10$:

$$5.0\text{ Mw Event} \times 10 = 50\text{ meters ground footprint radius}$$

This forces individual coordinate points to render as sharp, independent, and distinct hotspots, preserving clean spatial visibility even within dense seismic zones like the Pacific Ring of Fire.

---

## 📂 Repository File Architecture

```text
Earthquake-Trend-Analytics/
├── app.py                            # Core Streamlit & Visualization Engine
├── requirements.txt                  # Cloud Dependency Package Config
└── usgs_earthquake_trends_dataset.csv # Cleaned Multi-Decade Seismic Dataset
