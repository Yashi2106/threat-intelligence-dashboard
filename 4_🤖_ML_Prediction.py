import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from utils.data_loader import load_data
import plotly.express as px

st.set_page_config(page_title="ML Prediction", page_icon="🤖")

# Custom CSS for better design
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #4fc3f7;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #b0bec5;
        margin-bottom: 30px;
    }
    .card {
        background: linear-gradient(145deg, #1a2332, #0f1624);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #2a3a5c;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 10px 0;
    }
    .highlight {
        color: #4fc3f7;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 AI Threat Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Machine Learning model to predict attack patterns</div>', unsafe_allow_html=True)

df = load_data()

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Model Training")

# Prepare data for ML
# Select features for ML
features = ['iyear', 'country_txt', 'region_txt']
target = 'attacktype1_txt'

# Create feature matrix
X = df[features].copy()
y = df[target].copy()

# Encode categorical variables
label_encoders = {}
for col in ['country_txt', 'region_txt']:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Encode target
target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

# Check if we have enough data
if len(X) > 10:
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)
    rf.fit(X_train, y_train)
    
    # Predict
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Display results
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🎯 Model Accuracy", f"{accuracy:.2%}")
    with col2:
        st.metric("📊 Training Samples", f"{len(X_train):,}")
    
    st.markdown("---")
    
    # Feature Importance with USER-FRIENDLY NAMES
    st.subheader("🔑 Feature Importance")
    
    # BETTER NAMES for display (iyear → Year, country_txt → Country, region_txt → Region)
    feature_display_names = ['Year', 'Country', 'Region']
    
    importance_df = pd.DataFrame({
        'Feature': feature_display_names,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    fig = px.bar(
        importance_df,
        x='Importance',
        y='Feature',
        orientation='h',
        title='What factors most influence attack type?',
        template='plotly_dark',
        color='Importance',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        height=350, 
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Importance",
        yaxis_title="Factor"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 Random Forest model predicts attack type based on Year, Country, and Region")
else:
    st.warning("⚠️ Not enough data to train model. Please check your dataset.")
    
st.markdown('</div>', unsafe_allow_html=True)