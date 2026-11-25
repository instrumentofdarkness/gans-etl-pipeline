from src.database import (
    get_engine,
    load_cities,
    load_flights,
    load_populations,
    load_weather,
)
from src.flights import get_flights_data
from src.scraping import get_cities_data
from src.weather import get_weather_data

CITIES = ["Berlin", "Hamburg", "Munich"]


def main():
    engine = get_engine()

    print("1/3 Scraping city data...")
    cities_df = get_cities_data(CITIES)
    load_cities(cities_df, engine)
    load_populations(cities_df, engine)

    print("2/3 Fetching weather forecasts...")
    weather_df = get_weather_data(cities_df)
    load_weather(weather_df, engine)

    print("3/3 Fetching tomorrow's flight arrivals...")
    flights_df = get_flights_data()
    load_flights(flights_df, engine)

    print(
        f"Done: {len(cities_df)} cities, {len(weather_df)} weather rows, "
        f"{len(flights_df)} flights."
    )


if __name__ == "__main__":
    main()