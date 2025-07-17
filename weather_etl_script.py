import os
import requests
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# PostgreSQL connection
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)
cursor = conn.cursor()

# Fetch weather data function
def fetch_weather_data(start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "Asia/Kolkata"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and "hourly" in response.json():
        return response.json()
    else:
        print("API error:", response.status_code)
        return None

# Insert data into PostgreSQL
def insert_weather_data(data):
    hourly = data["hourly"]
    for i in range(len(hourly["time"])):
        if (hourly["temperature_2m"][i] is None or
            hourly["relative_humidity_2m"][i] is None or
            hourly["precipitation"][i] is None or
            hourly["wind_speed_10m"][i] is None):
            print(f"Skipping row {i} due to missing values.")
            continue

        cursor.execute(
            "INSERT INTO weather_data (timestamp, temperature, humidity, precipitation, wind_speed) VALUES (%s, %s, %s, %s, %s)",
            (
                hourly["time"][i],
                hourly["temperature_2m"][i],
                hourly["relative_humidity_2m"][i],
                hourly["precipitation"][i],
                hourly["wind_speed_10m"][i]
            )
        )
    conn.commit()


# Main ETL run example
if __name__ == "__main__":
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    weather_data = fetch_weather_data(yesterday.isoformat(), today.isoformat())
    if weather_data:
        insert_weather_data(weather_data)
        print("Data inserted successfully.")
    else:
        print("No data fetched.")
    cursor.close()
    conn.close()
