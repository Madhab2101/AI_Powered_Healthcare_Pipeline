from fastapi import FastAPI
import pandas as pd
import joblib
import uvicorn

app = FastAPI(
    title="AI-Powered Predictive Healthcare API",
    description="Real-time health risk prediction using Kafka, Spark, and AI models.",
    version="1.0"
)


model = joblib.load("D:/BDA/AI_Powered_Healthcare_Pipeline/models/model.pkl")

# Define columns used during training
FEATURE_COLS = [
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "oxygen_saturation",
    "body_temp",
    "glucose_level"
]

@app.get("/")
def root():
    return {"message": "AI-Powered Predictive Healthcare API is running"}

@app.post("/predict_batch")
def predict_batch(records: list[dict]):
    df = pd.DataFrame(records)

    # Keep only relevant features
    df_model = df[FEATURE_COLS].copy()

    # Predict raw numeric risk score
    preds = model.predict(df_model)

    #  Convert numeric predictions into labeled categories
    def map_risk(score):
        if score >= 0.6:
            return "High"
        elif score >= 0.45:
            return "Medium"
        else:
            return "Low"

    df["predicted_risk_score"] = preds  # keep numeric score
    df["predicted_risk"] = [map_risk(s) for s in preds]

    return df.to_dict(orient="records")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
