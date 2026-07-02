# Real-Time Transaction Fraud Detection Pipeline

Fraud classification pipeline on 590,000+ IEEE-CIS transactions. Served via FastAPI, containerised with Docker, deployed on Render with a Streamlit analyst interface.

**[Live Analyst Tool](https://financial-risk-analyser.streamlit.app)** | **[Live API](https://fraud-detection-api-tg28.onrender.com)** | **[API Docs](https://fraud-detection-api-tg28.onrender.com/docs)**

---

## Model Performance

| Metric | Value |
|---|---|
| ROC-AUC | 0.9262 |
| Precision (default threshold) | 0.88 |
| Recall (default threshold) | 0.47 |
| Recall (optimal threshold) | 0.75 |
| Optimal Threshold | 0.056 |
| Training Samples | 120,000 |
| Test Samples | 30,000 |

---

## Key Technical Decisions

**SMOTE for class imbalance.** Dataset has a 2.65% fraud rate — a naive model predicting "not fraud" always achieves 97.35% accuracy but catches zero fraud. SMOTE raises the training fraud rate to 16.67%. Applied to training data only; test set stays at 2.65% for honest evaluation.

**Threshold tuning over default 0.5.** Default threshold: 88% precision, 47% recall — missing 53% of fraud. Lowering to 0.056 raises recall to 75%. Missing real fraud is more costly than false positives in banking. This is a deliberate business decision, not a model limitation.

**XGBoost for tabular fraud data.** Gradient boosting handles complex feature interactions and anonymised behavioural signals more effectively than linear models or random forests on this dataset.

**Google Colab for initial sampling.** Full dataset is 667MB — exceeding available local RAM. 150,000 transactions sampled in Colab. All preprocessing and training performed locally thereafter.

---

## Streamlit Demo Limitation

The analyst tool exposes 6 key features for manual input; remaining features default to 0. In production, all 200 features would be populated automatically from the payment system. The demo illustrates analyst workflow, not standalone prediction accuracy.

---

## Methodology

**Data:** 150,000 transactions sampled from the IEEE-CIS Kaggle dataset. Transaction and identity tables merged on TransactionID — 434 raw features.

**Preprocessing:** 232 columns with >50% missing values dropped. Remaining nulls imputed (median for numeric, mode for categorical). 5 categorical columns label encoded. Final feature set: 200 features.

**Modelling:** XGBoost — 200 estimators, max depth 6, learning rate 0.1. Evaluated on ROC-AUC, precision, recall, F1. Threshold tuned to optimise fraud recall.

**Deployment:** FastAPI containerised with Docker, deployed on Render. Streamlit interface on Streamlit Cloud.

---

## API

```bash
curl -X POST https://fraud-detection-api-tg28.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "TransactionAmt": 150.0,
      "ProductCD": 1,
      "card3": 150,
      "V57": 0.5,
      "C12": 1.0,
      "V30": 0.5
    }
  }'
```

```json
{
  "fraud_probability": 0.2202,
  "is_fraud": true,
  "risk_level": "MEDIUM",
  "threshold_used": 0.0563
}
```

---

## Structure
```
fraud-detection/
├── app/
│   ├── main.py                  # FastAPI application
│   └── streamlit_app.py         # Streamlit analyst interface
├── data/
│   ├── raw/                     # IEEE-CIS dataset (Kaggle)
│   └── processed/               # Sampled dataset
├── models/
│   ├── fraud_model.pkl
│   ├── feature_names.pkl
│   └── threshold.pkl
├── notebooks/
│   └── fraud_detection.ipynb
├── Dockerfile
└── requirements.txt
```

---

## Run Locally

```bash
git clone https://github.com/atharvakatkar/fraud-detection.git
cd fraud-detection

# With Docker
docker build -t fraud-detection .
docker run -p 8000:8000 fraud-detection

# Without Docker
pip install fastapi uvicorn pandas numpy scikit-learn xgboost joblib
uvicorn app.main:app --reload --port 8000

# Streamlit
pip install streamlit requests
streamlit run app/streamlit_app.py
```

---

## Future Work

- Populate all 200 features in Streamlit demo for accurate standalone predictions
- MLflow experiment tracking for model versioning
- Feature drift detection to monitor model degradation
- Retrain on full 590,000 transaction dataset using cloud compute
- API authentication for production security

---

**Atharva Katkar** | [GitHub](https://github.com/atharvakatkar) | [LinkedIn](https://www.linkedin.com/in/ankatkar) | Macquarie University
