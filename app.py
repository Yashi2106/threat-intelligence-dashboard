import streamlit as st
from utils.data_loader import load_data, get_summary_stats

st.set_page_config(
    page_title="Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ========== CUSTOM CSS FOR BEAUTIFUL DESIGN ==========
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0e17;
    }
    
    /* Gradient Header */
    .header-container {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid #4fc3f7;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    .header-container h1 {
        color: #4fc3f7 !important;
        font-size: 3rem;
        margin: 0;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(79, 195, 247, 0.3);
    }
    .header-container p {
        color: #b0bec5 !important;
        font-size: 1.2rem;
        margin: 10px 0 0 0;
    }
    
    /* Cards */
    .custom-card {
        background: linear-gradient(145deg, #1a2332, #0f1624);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #2a3a5c;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        margin: 15px 0;
        transition: transform 0.2s;
    }
    .custom-card:hover {
        transform: translateY(-2px);
        border-color: #4fc3f7;
    }
    
    /* Metric Cards - Glass effect */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, rgba(26, 35, 50, 0.9), rgba(15, 22, 36, 0.9));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #2a3a5c;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-color: #4fc3f7;
        box-shadow: 0 4px 25px rgba(79, 195, 247, 0.2);
    }
    
    /* Metric labels */
    div[data-testid="metric-container"] label {
        color: #a8c8ff !important;
        font-weight: 600;
    }
    
    /* Metric values */
    div[data-testid="metric-container"] div {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* Headers */
    h1 { color: #4fc3f7 !important; }
    h2, h3, h4 {
        color: #e8f0ff !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e17, #141e2b);
        border-right: 1px solid #1a2a44;
    }
    section[data-testid="stSidebar"] * {
        color: #c0d8ff !important;
    }
    
    /* DataFrame - FIXED column headers */
    .stDataFrame {
        background: #0f1624;
        border-radius: 10px;
        border: 1px solid #1a2a44;
    }
    .stDataFrame thead tr th {
        color: #4fc3f7 !important;
        font-weight: 600;
        background-color: #0f1624 !important;
    }
    .stDataFrame tbody tr td {
        color: #e0e8f0 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #1a3a6a, #2a5a9a);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(79, 195, 247, 0.3);
    }
    
    /* Slider */
    .stSlider {
        color: #a8c8ff;
    }
    
    /* All text */
    .stMarkdown, p, li, label {
        color: #e0e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== CACHE DATA ==========
@st.cache_data
def load_cached_data():
    return load_data()

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("🛡️ Threat Intelligence")
    st.markdown("---")
    
    df = load_cached_data()
    years = sorted(df['iyear'].unique())
    
    selected_years = st.slider(
        "📅 Select Year Range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(2000, int(max(years)))
    )
    
    countries = ['All'] + sorted(df['country_txt'].unique().tolist())
    selected_country = st.selectbox("🌍 Select Country", countries)
    
    st.markdown("---")
    st.caption("🚀 Powered by GTD Dataset (1970-2020)")

# ========== MAIN PAGE ==========

# Beautiful Header
st.markdown("""
<div class="header-container">
    <h1>🛡️ Threat Intelligence Dashboard</h1>
    <p>AI-powered analysis of global terrorism patterns</p>
</div>
""", unsafe_allow_html=True)

# Filter data
filtered_df = df[
    (df['iyear'] >= selected_years[0]) & 
    (df['iyear'] <= selected_years[1])
]

if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['country_txt'] == selected_country]

# Metrics
stats = get_summary_stats(filtered_df)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Attacks", f"{stats['total_attacks']:,}")
with col2:
    st.metric("📉 Total Killed", f"{stats['total_killed']:,}")
with col3:
    st.metric("📈 Total Wounded", f"{stats['total_wounded']:,}")
with col4:
    st.metric("🌍 Countries", stats['countries'])

# Recent data with USER-FRIENDLY column names
st.markdown("---")
st.subheader("📋 Recent Incidents")

recent = filtered_df.sort_values('iyear', ascending=False).head(10)
if not recent.empty:
    # Create a copy with user-friendly column names
    display_df = recent[['iyear', 'country_txt', 'attacktype1_txt', 'nkill', 'nwound']].copy()
    display_df.columns = ['Year', 'Country', 'Attack Type', 'Killed', 'Wounded']  # FIXED: User-friendly names
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No data available")

st.caption("💡 Navigate to other pages using the sidebar above")