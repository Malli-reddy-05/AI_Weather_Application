import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from services.groq_service import explain_weather
from services.weather_service import WeatherServiceError, get_current_weather

load_dotenv()

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/weather")
def weather():
    payload = request.get_json(silent=True) or {}
    city = str(payload.get("city", "")).strip()

    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

    try:
        weather_data = get_current_weather(city)
        weather_data["summary"] = explain_weather(weather_data)
        return jsonify(weather_data)
    except WeatherServiceError as error:
        return jsonify({"error": str(error)}), error.status_code
    except Exception:
        app.logger.exception("Unexpected weather request error")
        return jsonify({"error": "Something went wrong. Please try again."}), 500


if __name__ == "__main__":
    app.run(debug=True)
