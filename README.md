# threat-intelligence-dashboard
AI-powered Threat Intelligence Dashboard analyzing 200,000+ global terrorism incidents (1970-2020) with interactive maps, machine learning predictions, and real-time threat alerts. Built with Streamlit, Python, and Scikit-learn.
# 🛡️ Threat Intelligence Dashboard

**Live Demo:** [https://threat-intelligence-dashboard-aisecurity.streamlit.app](https://threat-intelligence-dashboard-aisecurity.streamlit.app)

---

## 📌 Overview

An **AI-powered Threat Intelligence Dashboard** that analyzes global terrorism patterns from 1970 to 2020. This project combines data visualization, machine learning, and interactive mapping to provide actionable threat insights.

Built with **Python**, **Streamlit**, and **Scikit-learn**, the dashboard processes over **200,000+ terrorist incidents** and achieves **89.54% ML accuracy** in predicting weapon types.

---

## 🚀 Features

### 📊 Home Dashboard
- Key metrics: Total attacks, casualties, affected countries
- Interactive filters: Year range, country selection
- Recent incidents table with user-friendly column names

### 🗺️ Global Attack Map
- Interactive world map with attack locations
- Circle markers showing severity (size = casualties)
- Popup with incident details (year, attack type, killed)

### 📈 Country Analysis
- Attack trends over time for any country
- Attack type distribution (pie chart)
- Year-over-year pattern identification

### 🤖 AI Threat Prediction
- **Random Forest Classifier** with **89.54% accuracy**
- Predicts weapon type based on Year, Country, Region, and Attack Type
- Feature importance analysis (Attack Type is the strongest predictor)
- Trained on **127,000+** samples

### 🚨 Threat Alert System
- Threat score calculator (0-100) for any country
- Risk level classification: Low / Medium / High
- Recent incidents timeline with user-friendly columns

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Dashboard Framework | Streamlit |
| Machine Learning | Scikit-learn (Random Forest) |
| Data Processing | Pandas, NumPy |
| Visualizations | Plotly, Matplotlib |
| Mapping | Folium |
| Deployment | Streamlit Cloud |
| Version Control | Git, GitHub, Git LFS |

---

## 📊 Dataset

- **Source:** Global Terrorism Database (GTD)
- **Time Period:** 1970 - 2020
- **Records:** 200,000+ terrorist incidents
- **Size:** 150 MB (stored via Git LFS)

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.8+
- Git
- Git LFS (for dataset)

### Step 1: Clone the repository

```bash
git clone https://github.com/Yashi2106/threat-intelligence-dashboard.git
cd threat-intelligence-dashboard
python -m venv venv

# On Windows:
venv\Scripts\activate
pip install -r requirements.txt
python download_data.py
streamlit run app.py
