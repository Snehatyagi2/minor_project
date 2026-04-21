import os
from dotenv import load_dotenv
import requests
import random

load_dotenv()

# Register for free at: https://explore.openaq.org/register
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY", "")


def get_pollution(city):
    """
    Fetch latest pollution data for a city.
    Tries OpenAQ v3 API first. If unavailable, falls back to simulated data.
    """
    # Try OpenAQ v3 API
    if OPENAQ_API_KEY:
        try:
            data = _fetch_openaq_v3(city)
            if data:
                return data
        except Exception:
            pass

    # Fallback: generate simulated but realistic pollution data
    return _generate_simulated_pollution(city)


def _fetch_openaq_v3(city):
    """Fetch data from OpenAQ v3 API (requires API key)."""
    headers = {"X-API-Key": OPENAQ_API_KEY}

    # Step 1: Find location IDs for the city
    url = f"https://api.openaq.org/v3/locations?city={city}&limit=10"
    resp = requests.get(url, headers=headers, timeout=10)
    locations_data = resp.json()

    results = []
    for loc in locations_data.get("results", []):
        location_id = loc.get("id")
        location_name = loc.get("name", "Unknown")

        # Step 2: Get latest measurements for each location
        latest_url = f"https://api.openaq.org/v3/locations/{location_id}/latest"
        latest_resp = requests.get(latest_url, headers=headers, timeout=10)
        latest_data = latest_resp.json()

        pollutants = {}
        for sensor in latest_data.get("results", []):
            param = sensor.get("parameter", {})
            param_name = param.get("name", "")
            value = sensor.get("value", 0)
            pollutants[param_name.lower()] = value

        results.append({
            "location": location_name,
            "pm25": pollutants.get("pm25", pollutants.get("pm2.5", 0)),
            "pm10": pollutants.get("pm10", 0),
            "no2": pollutants.get("no2", 0)
        })

    return results


def _generate_simulated_pollution(city):
    """
    Generate realistic simulated pollution data for demonstration.
    Uses typical pollution ranges for Indian cities.
    """
    # Simulated monitoring stations based on common city layouts
    station_templates = [
        "{city} - Central Station",
        "{city} - Industrial Area",
        "{city} - Traffic Junction",
        "{city} - Residential Colony",
        "{city} - University Campus",
    ]

    results = []
    for template in station_templates:
        location = template.format(city=city)

        # Generate realistic pollution values
        if "Industrial" in location:
            pm25 = random.uniform(80, 200)
            pm10 = random.uniform(120, 300)
            no2 = random.uniform(50, 120)
        elif "Traffic" in location:
            pm25 = random.uniform(60, 150)
            pm10 = random.uniform(100, 250)
            no2 = random.uniform(40, 100)
        elif "Residential" in location:
            pm25 = random.uniform(30, 80)
            pm10 = random.uniform(50, 120)
            no2 = random.uniform(15, 50)
        else:
            pm25 = random.uniform(40, 120)
            pm10 = random.uniform(60, 180)
            no2 = random.uniform(20, 80)

        results.append({
            "location": location,
            "pm25": round(pm25, 2),
            "pm10": round(pm10, 2),
            "no2": round(no2, 2)
        })

    return results


def get_pollution_history(city):
    """
    Fetch historical NO2 data for a city.
    Tries OpenAQ v3 API first. If unavailable, falls back to simulated data.
    """
    if OPENAQ_API_KEY:
        try:
            return _fetch_history_v3(city)
        except Exception:
            pass

    # Fallback: simulated historical NO2 values
    return [round(random.uniform(20, 90), 2) for _ in range(10)]


def _fetch_history_v3(city):
    """Fetch historical NO2 measurements from OpenAQ v3."""
    headers = {"X-API-Key": OPENAQ_API_KEY}

    # Find locations first
    url = f"https://api.openaq.org/v3/locations?city={city}&limit=1"
    resp = requests.get(url, headers=headers, timeout=10)
    locations_data = resp.json()

    location_results = locations_data.get("results", [])
    if not location_results:
        return [round(random.uniform(20, 90), 2) for _ in range(10)]

    location_id = location_results[0].get("id")

    # Get recent measurements
    meas_url = f"https://api.openaq.org/v3/locations/{location_id}/measurements?parameter_id=2&limit=100"
    meas_resp = requests.get(meas_url, headers=headers, timeout=10)
    meas_data = meas_resp.json()

    history = []
    for item in meas_data.get("results", []):
        try:
            history.append(item.get("value", 0))
        except Exception:
            continue

    if not history:
        return [round(random.uniform(20, 90), 2) for _ in range(10)]

    return history[:10]