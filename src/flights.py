from datetime import date, timedelta

import pandas as pd
import requests

from src import config

HOST = "aerodatabox.p.rapidapi.com"
AIRPORTS = {"Berlin": "BER", "Hamburg": "HAM", "Munich": "MUC"}  # city -> IATA code


def get_flights_data(airports=AIRPORTS):
    """Return tomorrow's arrivals for each airport as a DataFrame."""
    tomorrow = date.today() + timedelta(days=1)
    headers = {"x-rapidapi-key": config.RAPIDAPI_KEY, "x-rapidapi-host": HOST}
    params = {
        "direction": "Arrival",
        "withCancelled": "false",
        "withCodeshared": "false",
        "withCargo": "false",
        "withPrivate": "false",
        "withLeg": "false",
        "withLocation": "false",
    }
    # The endpoint accepts at most a 12-hour window, so ask twice per airport
    windows = [("00:00", "11:59"), ("12:00", "23:59")]

    rows = []
    for city, iata in airports.items():
        for start, end in windows:
            url = (
                f"https://{HOST}/flights/airports/iata/{iata}/"
                f"{tomorrow}T{start}/{tomorrow}T{end}"
            )
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            for f in response.json().get("arrivals", []):
                movement = f.get("movement", {})
                origin = movement.get("airport", {})
                rows.append({
                    "city": city,
                    "flight_number": f.get("number"),
                    "origin_airport": origin.get("name"),
                    "origin_iata": origin.get("iata"),
                    "airline": (f.get("airline") or {}).get("name"),
                    "scheduled_arrival": (movement.get("scheduledTime") or {}).get("local"),
                    "status": f.get("status"),
                })

    df = pd.DataFrame(rows).dropna(subset=["flight_number", "scheduled_arrival"])
    # '2026-11-26 07:30+01:00' -> keep the local date and time, drop the offset
    df["scheduled_arrival"] = pd.to_datetime(df["scheduled_arrival"].str[:16])
    df["retrieval_date"] = date.today()
    return df.drop_duplicates(subset=["city", "flight_number", "scheduled_arrival"])