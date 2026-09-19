# AI Weather Assistant

A Flask web app that gets live weather from OpenWeather and explains it in everyday language using Groq.

## Setup

1. Create an [OpenWeather API key](https://openweathermap.org/api) and a [Groq API key](https://console.groq.com/keys).
2. Put them in `.env`:

   ```env
   OPENWEATHER_API_KEY=your_openweather_key
   GROQ_API_KEY=your_groq_key
   ```

3. Install and run:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python app.py
   ```

Open `http://127.0.0.1:5000` in a browser.

If Groq is not configured or unavailable, the app still shows a generated plain-language weather summary.

## Architecture

`Browser → Flask → OpenWeather (live data) → Groq (friendly explanation) → Browser`
