FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn pydantic pandas numpy scikit-learn xgboost imbalanced-learn joblib

# Copy app code and models
COPY app/ ./app/
COPY models/ ./models/

# Expose port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]