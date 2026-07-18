import streamlit as st
import folium
from streamlit_folium import folium_static
from utils.data_loader import load_data
import pandas as pd

st.set_page_config(page_title="World Map", page_icon="🗺️")

st.markdown("""
<style>
    .header-container {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #4fc3f7;
    }
    .header-container h1 {
        color: #4fc3f7 !important;
        font-size: 2.5rem;
        margin: 0;
    }
    .header-container p {
        color: #b0bec5 !important;
        margin: 5px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <h1>🗺️ Global Attack Map</h1>
    <p>Geographic distribution of terrorist incidents</p>
</div>
""", unsafe_allow_html=True)

df = load_data()

if df.empty:
    st.error("⚠️ No data available. Please check your dataset.")
    st.stop()

years = sorted(df['iyear'].unique())
year_range = st.slider(
    "📅 Select Year Range",
    min(years), max(years),
    (2000, max(years)),
    key="map"
)

filtered = df[(df['iyear'] >= year_range[0]) & (df['iyear'] <= year_range[1])]

m = folium.Map(location=[20, 10], zoom_start=2, tiles='CartoDB dark_matter')

for _, row in filtered.sample(min(1000, len(filtered))).iterrows():
    if pd.notna(row['latitude']) and pd.notna(row['longitude']):
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=max(2, min(12, row['nkill']/3 + 2)),
            color='#ff6b6b' if row['nkill'] > 10 else '#ffa94d',
            fill=True,
            fillColor='#ff6b6b' if row['nkill'] > 10 else '#ffa94d',
            fillOpacity=0.7,
            popup=f"""
            <div style="background:#1a2332; padding:10px; border-radius:10px; color:white;">
                <b>{row['country_txt']}</b><br>
                📅 Year: {row['iyear']}<br>
                🎯 Attack: {row['attacktype1_txt']}<br>
                💀 Killed: {row['nkill']}
            </div>
            """
        ).add_to(m)

folium_static(m, width=1000, height=600)
st.caption(f"📍 Showing {len(filtered)} incidents")
