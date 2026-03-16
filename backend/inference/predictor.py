import os
import logging
from pathlib import Path
import joblib
import pandas as pd
from dotenv import load_dotenv
from joblib import load


# load .env content to env vars
load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "model" / "cardio_prediction_model.joblib"

model = joblib.load(MODEL_PATH)

LOG_PATH = PROJECT_ROOT / "logs" / "app.log"

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH)
    ]
)

# load the trained model only once (module-level cache)
model = load(MODEL_PATH)
logging.info("Model loaded successfully.")

def predict(input_data: dict):

    df = pd.DataFrame([input_data])

    # get predicted class
    prediction = int(model.predict(df)[0])
    # get prediction probability
    probability = float(model.predict_proba(df)[0][1])

    logging.info(f"Model provided a prediction: {prediction}, probability: {probability}")

    return {
        "prediction": prediction,
        "probability": probability,
        "diagnosis": "High Cardio Risk Detected" if prediction == 1 else "Low Cardio Risk Detected"
    }


# example usage
# sample_input = {
#     "age": 52,
#     "sex": 1,
#     "cp": 0,
#     "trestbps": 125,
#     "chol": 212,
#     "fbs": 0,
#     "restecg": 1,
#     "thalach": 168,
#     "exang": 0,
#     "oldpeak": 1.0,
#     "slope": 2,
#     "ca": 0,
#     "thal": 2
# }
# result = predict(input_data=sample_input)
# print(result)