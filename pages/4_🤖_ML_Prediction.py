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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 AI Threat Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Machine Learning model to predict weapon types</div>', unsafe_allow_html=True)

df = load_data()

if df.empty:
    st.error("⚠️ No data available. Please check your dataset.")
    st.stop()

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Model Training")

features = ['iyear', 'country_txt', 'region_txt', 'attacktype1_txt']
target = 'weaptype1_txt'

X = df[features].copy()
y = df[target].copy()
y = y.fillna(y.mode()[0])

label_encoders = {}
for col in ['country_txt', 'region_txt', 'attacktype1_txt']:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

if len(X) > 10:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )
    
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Model Accuracy", f"{accuracy:.2%}")
    with col2:
        st.metric("📊 Training Samples", f"{len(X_train):,}")
    with col3:
        st.metric("🔧 Features Used", len(features))
    
    st.markdown("---")
    st.subheader("🔑 Feature Importance")
    
    feature_display_names = ['Year', 'Country', 'Region', 'Attack Type']
    
    importance_df = pd.DataFrame({
        'Feature': feature_display_names,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    fig = px.bar(
        importance_df,
        x='Importance',
        y='Feature',
        orientation='h',
        title='What factors most influence weapon choice?',
        template='plotly_dark',
        color='Importance',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🎯 Key Insights")
    top_features = importance_df.head(3)
    st.info(f"💡 {top_features.iloc[0]['Feature']} is the strongest predictor, followed by {top_features.iloc[1]['Feature']}")
    
else:
    st.warning("⚠️ Not enough data to train model.")

st.markdown('</div>', unsafe_allow_html=True)
