import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# Load model once
model = joblib.load("model/alzheimer_model.pkl")

app = FastAPI(title="Alzheimer Diagnosis API")

class HandwritingInput(BaseModel):
    features: list[float]  # same order as training features

@app.post("/predict")
def predict(data: HandwritingInput):
    X = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X).max()

    return {
        "prediction": int(prediction),
        "confidence": float(probability)
    }
