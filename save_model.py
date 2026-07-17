import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_data

def save_model():
    print("🔄 Training model...")
    df = load_data()
    
    # Features
    features = ['iyear', 'country_txt', 'region_txt', 'attacktype1_txt']
    target = 'weaptype1_txt'
    
    X = df[features].copy()
    y = df[target].copy()
    y = y.fillna(y.mode()[0])
    
    # Encode
    label_encoders = {}
    for col in ['country_txt', 'region_txt', 'attacktype1_txt']:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
    
    target_encoder = LabelEncoder()
    y_encoded = target_encoder.fit_transform(y)
    
    # Train model
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X, y_encoded)
    
    # Create models folder if doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save model
    joblib.dump(rf, 'models/threat_model.pkl')
    joblib.dump(label_encoders, 'models/label_encoders.pkl')
    joblib.dump(target_encoder, 'models/target_encoder.pkl')
    
    print("✅ Model saved successfully!")

if __name__ == "__main__":
    save_model()