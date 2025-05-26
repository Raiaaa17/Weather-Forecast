import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global variable to store weather data
cached_weather_data = None
last_update_time = None

def fetch_weather_data():
    """Fetch fresh weather data from the API"""
    OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    
    if not API_KEY:
        raise ValueError("OpenWeatherMap API key not found. Please set OPENWEATHERMAP_API_KEY in your .env file.")

    parameters = {
        "lat": 1.2966,  # NUS Kent Ridge campus coordinates
        "lon": 103.7764,
        "appid": API_KEY,
        "units": "metric"  # Add metric units for better temperature understanding
    }

    response = requests.get(OWM_Endpoint, params=parameters)
    response.raise_for_status()
    data = response.json()

    forecasts = data["list"]
    dic = {}
    for cast in forecasts:    
        weather = cast["weather"][0]["main"]
        temp = round(cast["main"]["temp"])  # Get temperature
        dt = datetime.strptime(cast["dt_txt"], "%Y-%m-%d %H:%M:%S")
        formatted_date = dt.strftime("%b %d")
        formatted_time = dt.strftime("%H.%M")

        if formatted_date not in dic:
            dic[formatted_date] = {}
        if formatted_time not in dic[formatted_date]:
            dic[formatted_date][formatted_time] = []
        dic[formatted_date][formatted_time].extend([weather, temp])
    
    return dic

def update_weather():
    """Update the cached weather data"""
    global cached_weather_data, last_update_time
    try:
        cached_weather_data = fetch_weather_data()
        last_update_time = datetime.now()
        print(f"Weather data updated at {last_update_time}")
    except Exception as e:
        print(f"Error updating weather data: {e}")

def get_weather():
    """Get weather data from cache or fetch new data if needed"""
    global cached_weather_data
    if cached_weather_data is None:
        update_weather()
    return cached_weather_data

get_weather()




