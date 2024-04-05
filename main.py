from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Create a FastAPI instance
app = FastAPI()

# Load the entire pipeline
sep_pipeline = joblib.load("./Model/RandomForestClassifier_pipeline.joblib")
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
def predict(PredictionInput: PredictionInput):
    df = pd.DataFrame([PredictionInput.model_dump()])
    # Make predictions using the pipeline
    prediction = sep_pipeline.predict(df)
    
    encode = encoder.inverse_transform([prediction])[0]
    
    # Return the prediction
    return {'prediction': encode }