import pandas as pd
import numpy as np
import streamlit as st
import os

@st.cache_data
def load_data():
    """Load GTD dataset"""
    
    # Check if file exists
    if not os.path.exists('data/gtd.csv'):
        st.warning("⚠️ Dataset not found! Please upload data/gtd.csv")
        return pd.DataFrame()
    
    try:
        columns_to_read = [
            'iyear', 'imonth', 'iday', 'country_txt', 'region_txt',
            'city', 'latitude', 'longitude', 'attacktype1_txt',
            'targtype1_txt', 'weaptype1_txt', 'nkill', 'nwound',
            'gname', 'success', 'suicide'
        ]
        
        df = pd.read_csv(
            'data/gtd.csv', 
            encoding='latin-1', 
            low_memory=False,
            usecols=lambda col: col in columns_to_read
        )
        
        df = df.dropna(subset=['country_txt', 'iyear'])
        df['nkill'] = df['nkill'].fillna(0)
        df['nwound'] = df['nwound'].fillna(0)
        df['latitude'] = df['latitude'].fillna(0)
        df['longitude'] = df['longitude'].fillna(0)
        df['iyear'] = df['iyear'].astype(int)
        df['nkill'] = df['nkill'].astype(int)
        df['nwound'] = df['nwound'].astype(int)
        df['total_casualties'] = df['nkill'] + df['nwound']
        df['decade'] = (df['iyear'] // 10) * 10
        df = df[df['iyear'] >= 1970]
        
        return df
        
    except Exception as e:
        st.error(f"⚠️ Error loading data: {str(e)}")
        return pd.DataFrame()

def get_summary_stats(df):
    if df.empty:
        return {'total_attacks': 0, 'total_killed': 0, 'total_wounded': 0, 'countries': 0, 'years': 'N/A'}
    
    return {
        'total_attacks': len(df),
        'total_killed': int(df['nkill'].sum()),
        'total_wounded': int(df['nwound'].sum()),
        'countries': df['country_txt'].nunique(),
        'years': f"{df['iyear'].min()} - {df['iyear'].max()}"
    }