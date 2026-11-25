import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (educational project; contact: your-email@example.com)"}


def clean_population(raw):
    """'3,596,999' -> 3596999 (drops footnote markers like [1])"""
    raw = raw.split("[")[0]
    return int(re.sub(r"\D", "", raw))


def dms_to_decimal(dms):
    """'52°31′12″N' -> 52.52 (S and W become negative)"""
    deg, minutes, seconds, direction = re.match(
        r"(\d+)°(?:(\d+)′)?(?:(\d+)″)?([NSEW])", dms
    ).groups()
    value = int(deg) + int(minutes or 0) / 60 + int(seconds or 0) / 3600
    return round(-value if direction in ("S", "W") else value, 4)


def get_infobox_value(infobox, label, next_row=False):
    """Return the text of the infobox row whose header contains `label`.
    With next_row=True, read the value from the row after the header."""
    rows = infobox.find_all("tr")
    for i, row in enumerate(rows):
        header = row.find("th")
        if header and label in header.get_text():
            target = rows[i + 1] if next_row else row
            return target.find("td").get_text(" ", strip=True)
    return None


def scrape_city(city):
    """Scrape one city's Wikipedia page and return a dict of clean values."""
    url = f"https://en.wikipedia.org/wiki/{city}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    infobox = soup.find("table", class_="infobox")

    return {
        "city": city,
        "country": get_infobox_value(infobox, "Country"),
        "population": clean_population(
            get_infobox_value(infobox, "Population", next_row=True)
        ),
        "latitude": dms_to_decimal(soup.find("span", class_="latitude").get_text()),
        "longitude": dms_to_decimal(soup.find("span", class_="longitude").get_text()),
    }


def get_cities_data(cities):
    """Take a list of city names, return a clean DataFrame."""
    rows = []
    for city in cities:
        try:
            rows.append(scrape_city(city))
        except Exception as e:
            print(f"Skipping {city}: {e}")
        time.sleep(1)  # be polite to Wikipedia
    return pd.DataFrame(rows)