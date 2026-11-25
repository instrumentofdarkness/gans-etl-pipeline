# Gans ETL Pipeline: Data for Predicting E-Scooter Movement

An end-to-end ETL (Extract, Transform, Load) pipeline that collects city, weather and flight data from external sources and stores it in a MySQL database. Built for **Gans**, an e-scooter-sharing startup, to support future predictive modelling of where scooters are needed.

> **Status:** In Progress | **Built with:** Python, BeautifulSoup, pandas, SQLAlchemy, MySQL

---

## Table of Contents
1. [Business Problem](#business-problem)
2. [Project Overview](#project-overview)
3. [Data Sources](#data-sources)
4. [Database Design](#database-design)
5. [Repository Structure](#repository-structure)
6. [Setup and Usage](#setup-and-usage)
7. [Challenges and Solutions](#challenges-and-solutions)
8. [Key Insights and Tips](#key-insights-and-tips)
9. [Skills Demonstrated](#skills-demonstrated)
10. [Possible Next Steps](#possible-next-steps)

---

## Business Problem

Gans operates e-scooters that users rent by the minute. Its success depends on having scooters **parked where users need them**. Several factors create imbalances:

- Hilly terrain (users ride uphill, walk downhill)
- Morning commutes from residential areas to the city centre
- Rain, which sharply reduces usage
- Tourists arriving by air who need scooters downtown or near landmarks

Before building predictive models, Gans needs data. This project collects external data that could help anticipate scooter movement and stores it in a structured, queryable form.

## Project Overview

The pipeline is built locally and follows the ETL pattern:

| Stage | What happens |
|-------|--------------|
| **Extract** | Scrape city data from Wikipedia; pull weather forecasts and flight arrivals from APIs |
| **Transform** | Clean and structure the data with pandas (string methods, regex, type conversion) |
| **Load** | Write the data into a relational MySQL database with proper keys and constraints |

## Data Sources

### 1. Web scraping: city demographics (Wikipedia)
- **Tool:** `requests` + `BeautifulSoup`
- **Cities:** Berlin, Hamburg, Munich
- **Fields:** population, latitude, longitude, country
- **Transform notes:** 

### 2. Weather: OpenWeather API
- **Endpoint:** 5-day / 3-hour forecast
- **Fields:** forecast time, outlook, temperature, feels-like, wind speed, rain probability
- **Transform notes:** 

### 3. Flights: AeroDataBox API (via RapidAPI)
- **Endpoint:** 
- **Fields:** 
- **Transform notes:** tomorrow's date is generated automatically and formatted to the endpoint's requirements

## Database Design

![ER diagram](docs/er_diagram.png)

| Table | Purpose | Key columns |
|-------|---------|-------------|
| `cities` | Static list of cities | `city_id` (PK), `city_name`, `country_code` |
| `populations` | Population over time, one row per city per year | `city_id` (FK), `population`, `timestamp_population` |
| `weather` | Forecast data | `id` (PK), `city_id` (FK), `forecast_time`, ... |
| `flights` | Arrivals per airport | `id` (PK), `city_id` (FK), ... |

## Repository Structure


gans-etl-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example          # template for API keys and DB credentials
├── main.py               # runs the full pipeline
├── notebooks/
│   ├── 01_web_scraping.ipynb
│   ├── 02_weather_api.ipynb
│   ├── 03_flights_api.ipynb
│   └── 04_database_load.ipynb
├── src/
│   ├── config.py         # loads credentials from environment variables
│   ├── scraping.py       # Wikipedia scraper
│   ├── weather.py        # OpenWeather extraction and cleaning
│   ├── flights.py        # AeroDataBox extraction and cleaning
│   └── database.py      # connection and loading functions
├── sql/
│   └── schema.sql        # CREATE TABLE statements
└── docs/
    └── er_diagram.png


## Setup and Usage

**Prerequisites:** Python 3.x, MySQL server running locally, an [OpenWeather](https://openweathermap.org/api) API key, and a [RapidAPI](https://rapidapi.com/) key with access to AeroDataBox.

## Challenges and Solutions

## Key Insights and Tips

## Skills Demonstrated

- Web scraping with BeautifulSoup
- Consuming REST APIs and navigating JSON
- Data cleaning with pandas string methods and regex
- Loops, list comprehensions and reusable functions in Python
- Designing a relational data model (tables, relationships)
- MySQL tables with appropriate data types, constraints, primary and foreign keys
- Loading data from Python into MySQL (SQLAlchemy / `.to_sql()` / INSERT queries)
- Documenting a project for a portfolio

## Possible Next Steps

