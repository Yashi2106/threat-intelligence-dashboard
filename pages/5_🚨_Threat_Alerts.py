import streamlit as st
import pandas as pd
from utils.data_loader import load_data

st.set_page_config(page_title="Threat Alerts", page_icon="🚨")

st.markdown("""
<style>
    .header-container {
        background: linear-gradient(135deg, #1a0a0a, #2c1515, #3a1a1a);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #ff6b6b;
    }
    .header-container h1 {
        color: #ff6b6b !important;
        font-size: 2.5rem;
        margin: 0;
    }
    .header-container p {
        color: #ffa8a8 !important;
        margin: 5px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <h1>🚨 Threat Alert System</h1>
    <p>Real-time threat monitoring and risk assessment</p>
</div>
""", unsafe_allow_html=True)

df = load_data()

if df.empty:
    st.error("⚠️ No data available. Please check your dataset.")
    st.stop()

st.subheader("📊 Threat Score Calculator")

countries = sorted(df['country_txt'].unique())
selected_country = st.selectbox("🌍 Select Country for Threat Assessment", countries)

country_df = df[df['country_txt'] == selected_country]

if not country_df.empty:
    total_attacks = len(country_df)
    total_killed = int(country_df['nkill'].sum())
    total_wounded = int(country_df['nwound'].sum())
    avg_casualties = (total_killed + total_wounded) / total_attacks if total_attacks > 0 else 0
    
    threat_score = min(100, (
        (total_attacks / 1000) * 20 +
        (total_killed / 500) * 40 +
        (avg_casualties / 10) * 40
    ))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💀 Total Killed", f"{total_killed:,}")
    with col2:
        st.metric("🩹 Total Wounded", f"{total_wounded:,}")
    with col3:
        threat_color = "🔴" if threat_score > 70 else "🟡" if threat_score > 40 else "🟢"
        st.metric("⚠️ Threat Score", f"{threat_score:.1f}/100", delta=threat_color)
    
    st.markdown("---")
    st.subheader("📈 Threat Level Gauge")
    
    if threat_score > 70:
        st.error(f"🚨 HIGH THREAT LEVEL: {selected_country} shows critical threat patterns")
    elif threat_score > 40:
        st.warning(f"⚠️ MEDIUM THREAT LEVEL: {selected_country} shows moderate threat patterns")
    else:
        st.success(f"✅ LOW THREAT LEVEL: {selected_country} shows relatively low threat patterns")
    
    st.progress(min(threat_score / 100, 1.0))
    
    st.markdown("---")
    st.subheader(f"📋 Recent Incidents in {selected_country}")
    
    recent = country_df.sort_values('iyear', ascending=False).head(10)
    if not recent.empty:
        display_df = recent[['iyear', 'attacktype1_txt', 'nkill', 'nwound', 'city']].copy()
        display_df.columns = ['Year', 'Attack Type', 'Killed', 'Wounded', 'City']
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No recent incidents")
else:
    st.warning("No data available for selected country")

st.caption("🚀 Threat score calculated based on attack frequency, fatalities, and severity")
