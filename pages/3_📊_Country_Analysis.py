import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Country Analysis", page_icon="📊")

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
    <h1>📊 Country-wise Threat Analysis</h1>
    <p>Deep dive into country-specific patterns</p>
</div>
""", unsafe_allow_html=True)

df = load_data()

if df.empty:
    st.error("⚠️ No data available. Please check your dataset.")
    st.stop()

countries = sorted(df['country_txt'].unique())
selected = st.selectbox("🌍 Select Country", countries)

country_df = df[df['country_txt'] == selected]

tab1, tab2 = st.tabs(["📈 Trends", "🎯 Attack Types"])

with tab1:
    yearly = country_df.groupby('iyear').size().reset_index(name='count')
    fig = px.line(
        yearly,
        x='iyear',
        y='count',
        title=f'Attacks in {selected} Over Time',
        template='plotly_dark',
        labels={'iyear': 'Year', 'count': 'Number of Attacks'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    attack_types = country_df['attacktype1_txt'].value_counts().reset_index()
    attack_types.columns = ['Attack Type', 'Count']
    fig = px.pie(
        attack_types,
        values='Count',
        names='Attack Type',
        title=f'Attack Types - {selected}',
        template='plotly_dark',
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    st.plotly_chart(fig, use_container_width=True)
