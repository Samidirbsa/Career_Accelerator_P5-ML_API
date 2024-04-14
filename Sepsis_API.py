from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Create a FastAPI instance
app = FastAPI()

# Load the RandomForestClassifier pipeline
rf_pipeline = joblib.load("./Model/RandomForestClassifier_pipeline.joblib")
# Load the XGBClassifier pipeline
xgb_pipeline = joblib.load("./Model/XGBClassifier_pipeline.joblib")
encoder = joblib.load("./Model/encoder.joblib")

# Define a FastAPI instance ML model input schema
class PredictionInput(BaseModel):
    PRG: int
    PL: int
    PR: int
    SK: int
    TS: int
    M11: float
    BD2: float
    Age: int
    Insurance: int

# Defining the root endpoint for the API
@app.get("/")
def index():
    explanation = {
        'message': "Welcome to the Sepsis Prediction App",
        'description': "This API allows you to predict sepsis based on patient data.",
    }
    return explanation

@app.post("/predict")
def predict(input_data: PredictionInput):
    # Create a DataFrame from input data
    df = pd.DataFrame([input_data.dict()])

    # Make predictions using the RandomForestClassifier pipeline
    rf_prediction = rf_pipeline.predict(df)
    # Make predictions using the XGBClassifier pipeline
    xgb_prediction = xgb_pipeline.predict(df)

    # Inverse transform the predictions using the encoder
    rf_prediction_label = encoder.inverse_transform(rf_prediction)[0]
    xgb_prediction_label = encoder.inverse_transform(xgb_prediction)[0]

    # Return the predictions
    return {'RandomForestClassifier_prediction': rf_prediction_label,
            'XGBClassifier_prediction': xgb_prediction_label}
