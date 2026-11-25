import pandas as pd
import requests

from src import config

URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather_data(cities_df):
    """Take a DataFrame with columns city, latitude, longitude.
    Return the 5-day / 3-hour forecast for every city as a DataFrame."""
    rows = []
    for c in cities_df.itertuples():
        params = {
            "lat": c.latitude,
            "lon": c.longitude,
            "appid": config.OPENWEATHER_API_KEY,
            "units": "metric",
        }
        response = requests.get(URL, params=params)
        response.raise_for_status()

        for item in response.json()["list"]:
            rows.append({
                "city": c.city,
                "forecast_time": item["dt_txt"],
                "outlook": item["weather"][0]["description"],
                "temperature": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "wind_speed": item["wind"]["speed"],
                "rain_prob": item["pop"],
            })

    df = pd.DataFrame(rows)
    df["forecast_time"] = pd.to_datetime(df["forecast_time"])
    return df