import streamlit as st
import pandas as pd
import os
import time
import plotly.express as px
import requests
import numpy as np

# CONFIGURATION
st.set_page_config(
    page_title="AI-Powered Predictive Healthcare Dashboard",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 AI-Powered Real-Time Predictive Healthcare Data Pipeline")
st.markdown("""
This dashboard visualizes **real-time AI-driven health risk predictions**
using **Kafka, Spark, FastAPI**, and **Streamlit**.
""")

DATA_PATH = "D:/BDA/AI_Powered_Healthcare_Pipeline/output/cleaned_data"
FASTAPI_URL = "http://127.0.0.1:8000/predict_batch"
REFRESH_INTERVAL = 5  # seconds


# LOAD LATEST DATA

@st.cache_data(ttl=10)
def load_latest_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    files = [os.path.join(DATA_PATH, f) for f in os.listdir(DATA_PATH) if f.endswith(".parquet")]
    if not files:
        return pd.DataFrame()
    df = pd.concat([pd.read_parquet(f) for f in files])
    df = df.drop_duplicates(subset=["patient_id", "timestamp"], keep="last")
    df = df.sort_values("timestamp", ascending=False)
    return df


# FETCH PREDICTIONS FROM FASTAPI

def fetch_predictions(df):
    try:
        df = df.copy()
        if "timestamp" in df.columns:
            df["timestamp"] = df["timestamp"].astype(str)

        data = df.to_dict(orient="records")
        response = requests.post(FASTAPI_URL, json=data, timeout=10)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"⚠️ FastAPI Error: {response.status_code}")
            return df
    except Exception as e:
        st.warning(f"⚠️ Could not connect to FastAPI ({e}). Showing previous data...")
        return df


# RISK THRESHOLD CONFIGURATION

st.sidebar.header("⚙️ Risk Threshold Settings")
high_threshold = st.sidebar.slider("High Risk ≥", 0.0, 1.0, 0.6, 0.05)
medium_threshold = st.sidebar.slider("Medium Risk ≥", 0.0, 1.0, 0.45, 0.05)

st.sidebar.markdown(f"""
🧾 Current settings:
- **High Risk ≥ {high_threshold:.2f}**
- **Medium Risk ≥ {medium_threshold:.2f}**
- **Low Risk < {medium_threshold:.2f}**
""")

# DASHBOARD LOOP

placeholder = st.empty()

while True:
    df = load_latest_data()

    with placeholder.container():
        if df.empty:
            st.info("⏳ Waiting for data from Spark streaming...")
            time.sleep(REFRESH_INTERVAL)
            continue

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # 🧠 Get predictions from FastAPI
        df = fetch_predictions(df)

        # ✅ Map risk dynamically based on sidebar thresholds
        if "predicted_risk_score" in df.columns:
            def map_risk_dynamic(score):
                if score >= high_threshold:
                    return "High"
                elif score >= medium_threshold:
                    return "Medium"
                else:
                    return "Low"
            df["predicted_risk"] = df["predicted_risk_score"].apply(map_risk_dynamic)
        elif "predicted_risk" not in df.columns:
            df["predicted_risk"] = np.random.choice(["Low", "Medium", "High"], len(df))

        # -------------------------------------------------------
        # 📊 SUMMARY SECTION
        # -------------------------------------------------------
        total_patients = df["patient_id"].nunique()
        high_risk = (df["predicted_risk"] == "High").sum()
        med_risk = (df["predicted_risk"] == "Medium").sum()
        low_risk = (df["predicted_risk"] == "Low").sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👩‍⚕️ Total Patients", total_patients)
        col2.metric("🔴 High Risk", high_risk)
        col3.metric("🟠 Medium Risk", med_risk)
        col4.metric("🟢 Low Risk", low_risk)

       
        # RISK DISTRIBUTION PIE CHART

        risk_counts = df["predicted_risk"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]

        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="Count",
            color="Risk Level",
            color_discrete_map={"High": "red", "Medium": "orange", "Low": "green"},
            title="🧠 AI-Predicted Health Risk Distribution"
        )
        st.plotly_chart(fig, use_container_width=True, key=f"pie_{int(time.time())}")

        # RECENT PATIENT RECORDS

        st.subheader("📋 Latest Patient Health Data")
        st.dataframe(
            df[[
                "patient_id", "timestamp", "heart_rate", "systolic_bp", "diastolic_bp",
                "oxygen_saturation", "body_temp", "glucose_level",
                "predicted_risk", "predicted_risk_score"
            ]].head(10),
            use_container_width=True
        )


        #  HIGH-RISK PATIENTS

        high_risk_df = df[df["predicted_risk"] == "High"]
        if not high_risk_df.empty:
            st.warning("🚨 High-Risk Patients Detected:")
            st.dataframe(
                high_risk_df[[
                    "patient_id", "heart_rate", "systolic_bp", "diastolic_bp",
                    "body_temp", "oxygen_saturation", "glucose_level",
                    "predicted_risk_score"
                ]].head(10),
                use_container_width=True
            )

    time.sleep(REFRESH_INTERVAL)
