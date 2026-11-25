CREATE DATABASE IF NOT EXISTS gans;
USE gans;

CREATE TABLE IF NOT EXISTS cities (
    city_id     INT AUTO_INCREMENT PRIMARY KEY,
    city_name   VARCHAR(100) NOT NULL UNIQUE,
    country     VARCHAR(100) NOT NULL,
    latitude    DECIMAL(7,4) NOT NULL,
    longitude   DECIMAL(7,4) NOT NULL
);

CREATE TABLE IF NOT EXISTS populations (
    population_id         INT AUTO_INCREMENT PRIMARY KEY,
    city_id               INT NOT NULL,
    population            INT NOT NULL,
    timestamp_population  INT NOT NULL,  -- year the figure was collected
    UNIQUE (city_id, timestamp_population),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE IF NOT EXISTS weather (
    weather_id     INT AUTO_INCREMENT PRIMARY KEY,
    city_id        INT NOT NULL,
    forecast_time  DATETIME NOT NULL,
    outlook        VARCHAR(100),
    temperature    DECIMAL(5,2),
    feels_like     DECIMAL(5,2),
    wind_speed     DECIMAL(5,2),
    rain_prob      DECIMAL(3,2),
    UNIQUE (city_id, forecast_time),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);
