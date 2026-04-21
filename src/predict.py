import pickle
import numpy as np
import pandas as pd
from src.api_pollution import get_pollution, get_pollution_history
from src.api_weather import get_weather
from src.logic import pollution_score, locality_type, detailed_reason


def load_model():
    with open("model/model.pkl","rb") as f:
        return pickle.load(f)
    

def satellite_downscaling(temp, humidity, lat, lon):
    from src.satellite import generate_satellite_grid

    model = load_model()
    grid = generate_satellite_grid(lat, lon)

    results = []

    for point in grid:
        data = pd.DataFrame([[point["no2"], temp, humidity]], columns=["NO2", "Temperature", "Humidity"])
        aqi = model.predict(data)[0]

        results.append({
            "lat": point["lat"],
            "lon": point["lon"],
            "aqi": round(aqi, 2)
        })

    return results


def predict_aqi(no2, temp, humidity):
    model = load_model()
    data = pd.DataFrame([[no2, temp, humidity]], columns=["NO2", "Temperature", "Humidity"])
    return float(model.predict(data)[0])


def smart_forecast(no2, temp, humidity, history):
    model = load_model()

    trend = sum(history[-3:]) / 3 if len(history) >= 3 else no2

    preds = []

    for i in range(1,8):
        adjusted_no2 = (no2 + trend)/2 + i*1.5
        adjusted_temp = temp + i*0.2
        adjusted_humidity = humidity + i*0.8

        data = pd.DataFrame([[adjusted_no2, adjusted_temp, adjusted_humidity]], columns=["NO2", "Temperature", "Humidity"])
        pred = model.predict(data)[0]
        preds.append(round(float(pred), 2))

    return preds


def generate_report(city="Delhi"):

    model = load_model()
    pollution = get_pollution(city)
    history = get_pollution_history(city)
    weather = get_weather(city)

    if not pollution or weather is None:
        return None

    temp, humidity, lat, lon = weather

    report = []

    for p in pollution:
        score = pollution_score(p["pm25"], p["pm10"], p["no2"])
        aqi = predict_aqi(p["no2"], temp, humidity)
        area = locality_type(p["location"])
        reason = detailed_reason(aqi, area, p["pm25"])

        forecast = smart_forecast(score, temp, humidity, history)

        report.append({
            "location": p["location"],
            "aqi": round(aqi,2),
            "score": round(score,2),
            "area": area,
            "forecast": forecast,
            "reason": reason
        })

    return report