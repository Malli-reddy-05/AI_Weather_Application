import os

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherServiceError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


def get_current_weather(city: str) -> dict:
    """Retrieve and normalize current conditions from OpenWeather."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherServiceError(
            "Weather service is not configured. Add OPENWEATHER_API_KEY to .env.", 503
        )

    try:
        response = requests.get(
            BASE_URL,
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10,
        )
    except requests.RequestException as error:
        raise WeatherServiceError("Unable to reach the weather service. Try again shortly.") from error

    if response.status_code == 404:
        raise WeatherServiceError("City not found. Check the spelling and try again.", 404)
    if response.status_code in (401, 403):
        raise WeatherServiceError("The weather API key is invalid or inactive.", 503)
    if not response.ok:
        raise WeatherServiceError("Weather data is temporarily unavailable. Please try again.")

    data = response.json()
    conditions = data.get("weather") or [{}]
    main = data.get("main") or {}
    wind = data.get("wind") or {}

    return {
        "city": data.get("name", city),
        "country": (data.get("sys") or {}).get("country", ""),
        "temperature": round(main.get("temp", 0)),
        "feels_like": round(main.get("feels_like", 0)),
        "humidity": main.get("humidity", 0),
        "wind_speed": round(wind.get("speed", 0) * 3.6, 1),
        "condition": conditions[0].get("main", "Unknown"),
        "description": conditions[0].get("description", "No description available").capitalize(),
        "icon": conditions[0].get("icon", "01d"),
    }
