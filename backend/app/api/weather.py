import os

import aiohttp

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"


async def get_weather_forecast(lat: float = 11.0, lon: float = 78.0) -> dict:
    if not OPENWEATHER_API_KEY:
        return {
            "source": "default",
            "location": {"lat": lat, "lon": lon},
            "current": {
                "temperature": 32.0,
                "humidity": 65.0,
                "condition": "partly cloudy",
                "wind_speed": 12.0,
                "rain_probability": 20.0,
            },
            "forecast": [],
            "note": "Set OPENWEATHER_API_KEY environment variable for live weather data",
        }

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{OPENWEATHER_BASE_URL}/weather", params=params) as resp:
            if resp.status != 200:
                return {"error": f"Weather API returned status {resp.status}"}
            current = await resp.json()

        async with session.get(f"{OPENWEATHER_BASE_URL}/forecast", params=params) as resp:
            if resp.status != 200:
                return {"error": f"Weather API returned status {resp.status}"}
            forecast_data = await resp.json()

    forecast_list = []
    if "list" in forecast_data:
        for item in forecast_data["list"][:5]:
            forecast_list.append({
                "datetime": item.get("dt_txt", ""),
                "temperature": item.get("main", {}).get("temp", 0),
                "humidity": item.get("main", {}).get("humidity", 0),
                "condition": item.get("weather", [{}])[0].get("description", ""),
                "rain_probability": item.get("pop", 0) * 100,
            })

    rain_prob = 0.0
    if forecast_list:
        rain_prob = max(f.get("rain_probability", 0) for f in forecast_list)

    return {
        "source": "openweathermap",
        "location": {"lat": lat, "lon": lon, "name": current.get("name", "Tamil Nadu")},
        "current": {
            "temperature": current.get("main", {}).get("temp", 0),
            "humidity": current.get("main", {}).get("humidity", 0),
            "condition": current.get("weather", [{}])[0].get("description", ""),
            "wind_speed": current.get("wind", {}).get("speed", 0),
            "rain_probability": rain_prob,
        },
        "forecast": forecast_list,
    }


def get_irrigation_advice(temperature: float, humidity: float, rain_probability: float, soil_type: str = "loam") -> str:
    advice_parts = []

    if temperature > 35:
        advice_parts.append("High temperature increases evapotranspiration. Irrigate in early morning (5-7 AM) or late evening (6-8 PM).")
    elif temperature > 28:
        advice_parts.append("Moderate water requirement. Irrigate during cooler parts of the day.")
    else:
        advice_parts.append("Normal irrigation schedule. Monitor soil moisture.")

    if humidity > 80:
        advice_parts.append("High humidity reduces water loss. Reduce irrigation frequency by 20-30%.")
    elif humidity < 40:
        advice_parts.append("Low humidity increases water stress. Increase irrigation frequency.")

    if rain_probability > 70:
        advice_parts.append(f"High rain probability ({rain_probability}%). Postpone irrigation for 24-48 hours.")
    elif rain_probability > 40:
        advice_parts.append(f"Moderate rain expected ({rain_probability}%). Reduce next irrigation by 30%.")

    if soil_type in ["sandy", "sandy_loam"]:
        advice_parts.append("Sandy soils drain quickly. Use smaller, more frequent irrigations.")
    elif soil_type in ["clay", "clay_loam"]:
        advice_parts.append("Clay soils retain water longer. Reduce irrigation frequency but increase duration.")

    return " ".join(advice_parts)


def get_disease_risk_forecast(temperature: float, humidity: float, rain_probability: float) -> dict:
    risk_factors = []
    overall_risk = "low"
    score = 0

    if 25 <= temperature <= 35 and humidity > 70:
        score += 2
        risk_factors.append("Warm humid conditions favor fungal diseases")
    elif temperature > 35:
        score += 1
        risk_factors.append("Heat stress weakens plant defenses")

    if humidity > 85:
        score += 3
        risk_factors.append("Very high humidity strongly favors disease development")
    elif humidity > 70:
        score += 2
        risk_factors.append("High humidity increases disease risk")
    elif humidity > 60:
        score += 1

    if rain_probability > 70:
        score += 2
        risk_factors.append("Rain splash spreads pathogens and creates leaf wetness")
    elif rain_probability > 40:
        score += 1

    if 20 <= temperature <= 30:
        score += 1
        risk_factors.append("Optimal temperature range for pathogen activity")

    if score >= 6:
        overall_risk = "high"
    elif score >= 3:
        overall_risk = "medium"
    elif score >= 1:
        overall_risk = "low"
    else:
        overall_risk = "minimal"

    high_risk_diseases = []
    if humidity > 70 and temperature > 25:
        high_risk_diseases.extend(["leaf_blight", "leaf_spot", "anthracnose"])
    if humidity > 80 and rain_probability > 50:
        high_risk_diseases.extend(["downy_mildew", "root_rot", "bacterial_blight"])
    if temperature > 30 and humidity > 60:
        high_risk_diseases.append("rust")

    return {
        "overall_risk": overall_risk,
        "risk_score": score,
        "risk_factors": risk_factors,
        "high_risk_diseases": list(set(high_risk_diseases)),
        "recommendations": _get_disease_recommendations(overall_risk),
    }


def _get_disease_recommendations(risk_level: str) -> list[str]:
    if risk_level == "high":
        return [
            "Apply preventive fungicide spray within 24 hours",
            "Monitor fields daily for early disease symptoms",
            "Improve field drainage to reduce humidity",
            "Prune dense canopy to improve air circulation",
            "Avoid overhead irrigation",
        ]
    elif risk_level == "medium":
        return [
            "Scout fields every 2-3 days for disease symptoms",
            "Prepare fungicide spray materials in advance",
            "Remove crop debris that may harbor pathogens",
            "Maintain proper spacing between plants",
        ]
    elif risk_level == "low":
        return [
            "Continue regular field monitoring",
            "Maintain good agricultural practices",
            "Keep field sanitation standards high",
        ]
    else:
        return [
            "Maintain current good practices",
            "No immediate disease management actions needed",
        ]
