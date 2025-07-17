from fastapi import FastAPI
from app.schemas import WeatherFeatures, PredictionResponse
from app.model_loader import predict_temperature

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "API is running"}

@app.post("/predict", response_model=PredictionResponse)
def predict(features: WeatherFeatures):
    prediction = predict_temperature(features.dict())
    return PredictionResponse(predicted_temperature=prediction)
