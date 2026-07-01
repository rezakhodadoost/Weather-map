import requests
# Maps Open-Meteo weather codes to readable descriptions and icon names.
WEATHER_CODES = {
    0: ("Clear Sky", "sun"),
    1: ("Mainly Clear", "sun"),
    2: ("Partly Cloudy", "cloud"),
    3: ("Overcast", "cloud"),
    45: ("Fog", "fog"),
    48: ("Depositing Rime Fog", "fog"),
    51: ("Light Drizzle", "drizzle"),
    53: ("Moderate Drizzle", "drizzle"),
    55: ("Dense Drizzle", "drizzle"),
    61: ("Slight Rain", "rain"),
    63: ("Moderate Rain", "rain"),
    65: ("Heavy Rain", "rain"),
    71: ("Snow", "snow"),
    80: ("Rain Showers", "rain"),
    95: ("Thunderstorm", "storm"),
}


def get_weather(latitude, longitude):
    # Request current weather data from the Open-Meteo API.
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&current=temperature_2m,"
        f"apparent_temperature,"
        f"relative_humidity_2m,"
        f"surface_pressure,"
        f"wind_speed_10m,"
        f"weather_code"
    )

    response = requests.get(url)
    data = response.json()

    current = data["current"]

    description, icon = WEATHER_CODES.get(
        current["weather_code"],
        ("Unknown", "unknown")
    )

    return {
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "pressure": current["surface_pressure"],
        "wind_speed": current["wind_speed_10m"],
        "description": description,
        "icon": icon,
    }