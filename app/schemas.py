from pydantic import BaseModel

class WeatherFeatures(BaseModel):
    temperature: float
    humidity: float
    precipitation: float
    wind_speed: float

class PredictionResponse(BaseModel):
    predicted_temperature: float
