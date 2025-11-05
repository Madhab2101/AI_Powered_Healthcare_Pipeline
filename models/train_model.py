import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

data = pd.DataFrame({
    "heart_rate": np.random.randint(60,120,1000),
    "systolic_bp": np.random.randint(100,160,1000),
    "diastolic_bp": np.random.randint(60,100,1000),
    "oxygen_saturation": np.random.uniform(92,100,1000),
    "body_temp": np.random.uniform(36,39,1000),
    "glucose_level": np.random.randint(70,160,1000)
})
data["risk_score"] = (
    0.3*(data["heart_rate"]/120) +
    0.2*(data["systolic_bp"]/160) +
    0.2*(data["glucose_level"]/160) +
    0.3*(1 - data["oxygen_saturation"]/100)
)

X = data.drop("risk_score", axis=1)
y = data["risk_score"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

os.makedirs("D:/BDA/AI_Powered_Healthcare_Pipelinene/models", exist_ok=True)
joblib.dump(model, "D:/BDA/AI_Powered_Healthcare_Pipelinene/models/model.pkl")

print(" Model trained and saved → models/model.pkl")
