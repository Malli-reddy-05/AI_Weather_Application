import os

from groq import Groq


def explain_weather(weather: dict) -> str:
    """Turn raw weather measurements into a short, practical explanation."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _fallback_summary(weather)

    prompt = (
        "Give a warm, practical weather note in no more than two sentences. "
        "Do not mention being an AI or give medical advice. "
        f"Location: {weather['city']}. Condition: {weather['description']}. "
        f"Temperature: {weather['temperature']}°C, feels like {weather['feels_like']}°C. "
        f"Humidity: {weather['humidity']}%. Wind: {weather['wind_speed']} km/h."
    )
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=100,
        )
        content = completion.choices[0].message.content
        return content.strip() if content else _fallback_summary(weather)
    except Exception:
        return _fallback_summary(weather)


def _fallback_summary(weather: dict) -> str:
    return (
        f"It is {weather['description'].lower()} and {weather['temperature']}°C in "
        f"{weather['city']}. Humidity is {weather['humidity']}% with winds near "
        f"{weather['wind_speed']} km/h."
    )
