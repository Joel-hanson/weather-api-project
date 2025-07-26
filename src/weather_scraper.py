import json
import os
import random
import re
import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup


def scrape_weather_data():
    """Scrape weather data from a public weather service"""
    try:
        # Configuration - customize for your location
        city = "New York"
        url = f"https://wttr.in/{city}?format=j1"  # JSON weather API

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; WeatherBot/1.0; +https://github.com/joel-hanson/weather-api-project)",
            "Accept": "application/json",
        }

        # Respectful delay
        time.sleep(random.uniform(1, 2))

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        weather_data = response.json()

        # Process and clean the data
        current_weather = extract_current_weather(weather_data)
        forecast_data = extract_forecast_data(weather_data)

        # Save current weather to API endpoint
        current_api = {
            "location": city,
            "last_updated": datetime.now().isoformat(),
            "current": current_weather,
        }

        # Save forecast to API endpoint
        forecast_api = {
            "location": city,
            "last_updated": datetime.now().isoformat(),
            "forecast": forecast_data,
        }

        # Ensure api directory exists
        os.makedirs("api", exist_ok=True)

        # Write to API files
        with open("api/current.json", "w") as f:
            json.dump(current_api, f, indent=2)

        with open("api/forecast.json", "w") as f:
            json.dump(forecast_api, f, indent=2)

        # Update historical data
        update_historical_weather(current_weather)

        print(f"Successfully updated weather data for {city}")
        return True

    except Exception as e:
        print(f"Error scraping weather data: {e}")
        return False


def extract_current_weather(data):
    """Extract current weather conditions"""
    current = data.get("current_condition", [{}])[0]

    return {
        "temperature_f": int(current.get("temp_F", 0)),
        "temperature_c": int(current.get("temp_C", 0)),
        "condition": current.get("weatherDesc", [{}])[0].get("value", "Unknown"),
        "humidity": int(current.get("humidity", 0)),
        "wind_speed_mph": int(current.get("windspeedMiles", 0)),
        "wind_direction": current.get("winddir16Point", "N"),
        "feels_like_f": int(current.get("FeelsLikeF", 0)),
        "feels_like_c": int(current.get("FeelsLikeC", 0)),
        "uv_index": int(current.get("uvIndex", 0)),
        "visibility_miles": int(current.get("visibility", 0)),
        "pressure_mb": int(current.get("pressure", 0)),
    }


def extract_forecast_data(data):
    """Extract 3-day forecast"""
    forecast = []

    for day_data in data.get("weather", [])[:3]:  # 3-day forecast
        date = day_data.get("date")
        hourly = day_data.get("hourly", [{}])
        astronomy = day_data.get("astronomy", [{}])[0]

        forecast.append(
            {
                "date": date,
                "max_temp_f": int(day_data.get("maxtempF", 0)),
                "min_temp_f": int(day_data.get("mintempF", 0)),
                "max_temp_c": int(day_data.get("maxtempC", 0)),
                "min_temp_c": int(day_data.get("mintempC", 0)),
                "condition": (
                    hourly[0].get("weatherDesc", [{}])[0].get("value", "Unknown")
                    if hourly
                    else "Unknown"
                ),
                "chance_of_rain": (
                    int(hourly[0].get("chanceofrain", 0)) if hourly else 0
                ),
                "chance_of_snow": (
                    int(hourly[0].get("chanceofsnow", 0)) if hourly else 0
                ),
                "max_wind_speed_mph": (
                    int(hourly[0].get("windspeedMiles", 0)) if hourly else 0
                ),
                "sunrise": astronomy.get("sunrise", ""),
                "sunset": astronomy.get("sunset", ""),
                "moon_phase": astronomy.get("moon_phase", ""),
                "moonrise": astronomy.get("moonrise", ""),
                "moonset": astronomy.get("moonset", ""),
            }
        )

    return forecast


def update_historical_weather(current_weather):
    """Maintain historical weather data"""
    try:
        with open("data/historical_weather.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    # Add new data with timestamp
    history.append(
        {
            "timestamp": datetime.now().isoformat(),
            "temperature_f": current_weather["temperature_f"],
            "temperature_c": current_weather["temperature_c"],
            "condition": current_weather["condition"],
            "humidity": current_weather["humidity"],
            "wind_speed_mph": current_weather["wind_speed_mph"],
        }
    )

    # Keep only last 7 days (168 hours if hourly updates)
    cutoff = datetime.now() - timedelta(days=7)
    history = [
        entry
        for entry in history
        if datetime.fromisoformat(entry["timestamp"]) > cutoff
    ]

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    with open("data/historical_weather.json", "w") as f:
        json.dump(history, f, indent=2)


def validate_weather_data(current, forecast):
    """Validate weather data quality"""
    # Check current weather
    if not current.get("temperature_f") or not current.get("condition"):
        raise ValueError("Missing essential current weather data")

    # Check temperature ranges
    temp_f = current.get("temperature_f", 0)
    if temp_f < -100 or temp_f > 150:  # Reasonable temperature range
        raise ValueError(f"Temperature out of range: {temp_f}°F")

    # Check forecast
    if not forecast or len(forecast) == 0:
        raise ValueError("No forecast data available")

    return True


if __name__ == "__main__":
    print("Starting weather data collection...")
    success = scrape_weather_data()

    if success:
        print("Weather data collection completed successfully!")
        exit(0)
    else:
        print("Weather data collection failed!")
        exit(1)
