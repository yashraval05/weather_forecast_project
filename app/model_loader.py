import tensorflow as tf
import numpy as np

# Load the model once at startup
model = tf.keras.models.load_model("models/weather_forecast_model.h5")
# Actual scaler min and max values for temperature based on training
temperature_min = 17.9
temperature_max = 39.1
# Define feature order for consistency
FEATURE_COLUMNS = ['temperature', 'humidity', 'precipitation', 'wind_speed']
SEQUENCE_LENGTH = 24  # As used in training

def inverse_scale_temperature(normalized_temp: float) -> float:
    return normalized_temp * (temperature_max - temperature_min) + temperature_min

def predict_temperature(features: dict) -> float:
    feature_values = [features[col] for col in FEATURE_COLUMNS]
    dummy_sequence = np.array([feature_values] * SEQUENCE_LENGTH).reshape(1, SEQUENCE_LENGTH, len(FEATURE_COLUMNS))
    normalized_prediction = model.predict(dummy_sequence)[0][0]
    actual_temperature = inverse_scale_temperature(normalized_prediction)
    return float(actual_temperature)