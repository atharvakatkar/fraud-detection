# 🔍 Fraud Detection API

[![Live API](https://img.shields.io/badge/Live%20API-Render-brightgreen)](https://fraud-detection-api-tg28.onrender.com)
[![API Docs](https://img.shields.io/badge/API%20Docs-Swagger-orange)](https://fraud-detection-api-tg28.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-red)](https://xgboost.readthedocs.io/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED)](https://www.docker.com/)

A real-time fraud detection API built with XGBoost and deployed via Docker on Render. Trained on the IEEE-CIS Fraud Detection competition dataset with 150,000 transactions and 200 features.

🔗 **[Live API](https://fraud-detection-api-tg28.onrender.com)**
📖 **[API Documentation](https://fraud-detection-api-tg28.onrender.com/docs)**

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status and model info |
| GET | `/health` | Health check |
| POST | `/predict` | Predict fraud probability for a transaction |
| GET | `/model-info` | Model metadata and performance metrics |

---

## Quick Start
```bash
curl -X POST https://fraud-detection-api-tg28.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "TransactionAmt": 150.0,
      "ProductCD": 1,
      "card3": 150,
      "V57": 0.5,
      "C12": 1.0
    }
  }'
```

**Response:**
```json
{
  "transaction_id": "unknown",
  "fraud_probability": 0.2202,
  "is_fraud": true,
  "risk_level": "MEDIUM",
  "threshold_used": 0.0563
}
```

---

## Model Performance

| Metric | Value |
|---|---|
| ROC-AUC | 0.9262 |
| Precision (Fraud) | 0.88 |
| Recall (Fraud) | 0.47 |
| Recall at Optimal Threshold | 0.75 |
| Optimal Threshold | 0.056 |

---

## Key Technical Decisions

**SMOTE for class imbalance.** The dataset has a 2.65% fraud rate — a model predicting "not fraud" for everything achieves 97.35% accuracy but catches zero fraud. SMOTE synthetically generates fraud examples in the training set, raising the fraud rate to 16.67% and significantly improving recall.

**Threshold tuning.** Default classification threshold of 0.5 achieves 88% precision but only 47% recall — missing 53% of fraud. Lowering the threshold to 0.056 raises recall to 75% at the cost of more false positives. In banking, missing fraud is more costly than false alarms.

**XGBoost over Random Forest.** XGBoost's gradient boosting handles the complex feature interactions in the IEEE-CIS dataset more effectively than Random Forest, achieving 0.926 ROC-AUC vs ~0.88 for Random Forest on this dataset.

**SMOTE applied to training set only.** Applying SMOTE to the full dataset before splitting would cause data leakage — synthetic fraud examples from the test set would appear in training. SMOTE is applied exclusively to the training set, keeping the test set at the real 2.65% fraud rate for honest evaluation.

---

## Methodology

**Data:** 150,000 transactions sampled from the IEEE-CIS Fraud Detection competition dataset (590,000 total). Initial sampling performed in Google Colab due to hardware constraints — documented as a resourcefulness signal, not a limitation. Identity and transaction datasets merged on TransactionID.

**Preprocessing:** 232 columns with more than 50% missing values dropped. Remaining nulls imputed with median for numeric columns and mode for categorical. 5 categorical columns label encoded.

**Feature Engineering:** 200 features used after cleaning. Top predictors are anonymous V and C columns — consistent with real fraud detection systems where behavioral signals are kept proprietary to prevent fraudsters gaming the system.

**Deployment:** FastAPI endpoint containerised with Docker and deployed on Render. Auto-generated Swagger documentation available at `/docs`.

---

## Project Structure
```
fraud-detection/
├── app/
│   └── main.py               # FastAPI application
├── data/
│   ├── raw/                  # IEEE-CIS dataset (not pushed — see Kaggle)
│   └── processed/            # Sampled dataset
├── models/
│   ├── fraud_model.pkl       # Trained XGBoost model
│   ├── feature_names.pkl     # Feature names for API input
│   └── threshold.pkl         # Optimal classification threshold
├── notebooks/
│   └── fraud_detection.ipynb # Full analysis and training notebook
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## How to Run Locally
```bash
# Clone the repository
git clone https://github.com/atharvakatkar/fraud-detection.git
cd fraud-detection

# Option 1 — Run with Docker
docker build -t fraud-detection .
docker run -p 8000:8000 fraud-detection

# Option 2 — Run without Docker
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` to test the API.

---

## Future Work

- Add a Streamlit demo frontend for non-technical users
- Implement MLflow for experiment tracking and model versioning
- Add feature drift detection to monitor model performance over time
- Retrain on full 590,000 transaction dataset using cloud compute
- Add authentication to the API endpoint

---

## Tech Stack

Python, XGBoost, Scikit-Learn, imbalanced-learn, FastAPI, Pydantic, Docker, Render, Pandas, NumPy, Google Colab

---

## Author

**Atharva Katkar**
[GitHub](https://github.com/atharvakatkar)

*Data Science Student — Macquarie University*