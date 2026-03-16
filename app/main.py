from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any

# LOAD MODEL ARTIFACTS
model = joblib.load("models/fraud_model.pkl")
feature_names = joblib.load("models/feature_names.pkl")
threshold = joblib.load("models/threshold.pkl")

# FASTAPI APP
app = FastAPI(
    title="Fraud Detection API",
    description="Real-time fraud detection using XGBoost trained on IEEE-CIS dataset",
    version="1.0.0",
)


# REQUEST SCHEMA
class Transaction(BaseModel):
    features: Dict[str, Any]


# RESPONSE SCHEMA
class FraudPrediction(BaseModel):
    transaction_id: str
    fraud_probability: float
    is_fraud: bool
    risk_level: str
    threshold_used: float


@app.get("/")
def root():
    return {
        "message": "Fraud Detection API",
        "status": "active",
        "model": "XGBoost",
        "roc_auc": 0.9262,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=FraudPrediction)
def predict(transaction: Transaction):
    try:
        # Build input dataframe with correct feature order
        input_dict = {feat: transaction.features.get(feat, 0) for feat in feature_names}
        input_df = pd.DataFrame([input_dict])

        # Predict
        fraud_proba = model.predict_proba(input_df)[0][1]
        is_fraud = bool(fraud_proba >= threshold)

        # Risk level
        if fraud_proba < 0.1:
            risk_level = "LOW"
        elif fraud_proba < 0.3:
            risk_level = "MEDIUM"
        elif fraud_proba < 0.6:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"

        return FraudPrediction(
            transaction_id=str(transaction.features.get("TransactionID", "unknown")),
            fraud_probability=round(float(fraud_proba), 4),
            is_fraud=is_fraud,
            risk_level=risk_level,
            threshold_used=round(float(threshold), 4),
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/model-info")
def model_info():
    return {
        "model_type": "XGBoost Classifier",
        "training_data": "IEEE-CIS Fraud Detection Dataset",
        "features": len(feature_names),
        "roc_auc": 0.9262,
        "threshold": round(float(threshold), 4),
        "smote_applied": True,
        "fraud_rate_training": "2.65%",
    }
