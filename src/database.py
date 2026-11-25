from datetime import datetime
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text

from src import config


def get_engine():
    url = (
        f"mysql+pymysql://{config.DB_USER}:{quote_plus(config.DB_PASSWORD)}"
        f"@{config.DB_HOST}/{config.DB_NAME}"
    )
    return create_engine(url)


def load_cities(df, engine):
    """Insert cities; update coordinates/country if the city already exists."""
    records = (
        df[["city", "country", "latitude", "longitude"]]
        .rename(columns={"city": "city_name"})
        .to_dict("records")
    )
    sql = text("""
        INSERT INTO cities (city_name, country, latitude, longitude)
        VALUES (:city_name, :country, :latitude, :longitude)
        ON DUPLICATE KEY UPDATE
            country = VALUES(country),
            latitude = VALUES(latitude),
            longitude = VALUES(longitude)
    """)
    with engine.begin() as conn:
        conn.execute(sql, records)


def load_populations(df, engine):
    """Insert this year's population per city (skips duplicates on rerun)."""
    with engine.connect() as conn:
        ids = pd.read_sql(text("SELECT city_id, city_name FROM cities"), conn)

    merged = df.merge(ids, left_on="city", right_on="city_name")
    records = [
        {
            "city_id": int(row.city_id),
            "population": int(row.population),
            "year": datetime.now().year,
        }
        for row in merged.itertuples()
    ]
    sql = text("""
        INSERT IGNORE INTO populations (city_id, population, timestamp_population)
        VALUES (:city_id, :population, :year)
    """)
    with engine.begin() as conn:
        conn.execute(sql, records)

def load_weather(df, engine):
    """Insert forecasts; update the values if the same city and time already exist."""
    with engine.connect() as conn:
        ids = pd.read_sql(text("SELECT city_id, city_name FROM cities"), conn)

    merged = df.merge(ids, left_on="city", right_on="city_name")
    records = [
        {
            "city_id": int(r.city_id),
            "forecast_time": r.forecast_time.to_pydatetime(),
            "outlook": r.outlook,
            "temperature": float(r.temperature),
            "feels_like": float(r.feels_like),
            "wind_speed": float(r.wind_speed),
            "rain_prob": float(r.rain_prob),
        }
        for r in merged.itertuples()
    ]
    sql = text("""
        INSERT INTO weather
            (city_id, forecast_time, outlook, temperature, feels_like, wind_speed, rain_prob)
        VALUES
            (:city_id, :forecast_time, :outlook, :temperature, :feels_like, :wind_speed, :rain_prob)
        ON DUPLICATE KEY UPDATE
            outlook = VALUES(outlook),
            temperature = VALUES(temperature),
            feels_like = VALUES(feels_like),
            wind_speed = VALUES(wind_speed),
            rain_prob = VALUES(rain_prob)
    """)
    with engine.begin() as conn:
        conn.execute(sql, records)