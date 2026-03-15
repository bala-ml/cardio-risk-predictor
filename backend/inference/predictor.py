import logging
from pathlib import Path

import pandas as pd
from joblib import load


# Path to model file
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "cardio_prediction_model.joblib"

# Logging setup (Render-safe)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

# Load model once
model = load(MODEL_PATH)
logging.info("Model loaded successfully.")


def predict(input_data: dict):

    df = pd.DataFrame([input_data])

    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    logging.info(f"Prediction: {prediction}, probability: {probability}")

    return {
        "prediction": prediction,
        "probability": probability
    }