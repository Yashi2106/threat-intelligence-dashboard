import pandas as pd
import numpy as np

def load_data():
    """Load and clean GTD dataset with optimized columns"""
    
    # Load only needed columns to save memory
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
    
    # Clean data
    df = df.dropna(subset=['country_txt', 'iyear'])
    
    # Fill missing values
    df['nkill'] = df['nkill'].fillna(0)
    df['nwound'] = df['nwound'].fillna(0)
    df['latitude'] = df['latitude'].fillna(0)
    df['longitude'] = df['longitude'].fillna(0)
    
    # Convert types
    df['iyear'] = df['iyear'].astype(int)
    df['nkill'] = df['nkill'].astype(int)
    df['nwound'] = df['nwound'].astype(int)
    
    # Add derived columns
    df['total_casualties'] = df['nkill'] + df['nwound']
    df['decade'] = (df['iyear'] // 10) * 10
    
    # Filter out years with no data
    df = df[df['iyear'] >= 1970]
    
    return df

def get_summary_stats(df):
    """Get summary statistics"""
    return {
        'total_attacks': len(df),
        'total_killed': int(df['nkill'].sum()),
        'total_wounded': int(df['nwound'].sum()),
        'countries': df['country_txt'].nunique(),
        'years': f"{df['iyear'].min()} - {df['iyear'].max()}"
    }