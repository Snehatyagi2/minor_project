import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    if not API_KEY:
        return None

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    try:
        return data["main"]["temp"], data["main"]["humidity"], data["coord"]["lat"], data["coord"]["lon"]
    except:
        return None
