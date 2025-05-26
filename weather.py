import os
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global variable to store weather data
cached_weather_data = None
last_update_time = None

def get_weather_icon(condition):
    """Get appropriate weather icon based on condition."""
    icons = {
        'Clear': 'sun',
        'Clouds': 'cloud',
        'Rain': 'cloud-rain',
        'Snow': 'snowflake',
        'Thunderstorm': 'bolt',
        'Drizzle': 'cloud-rain',
        'Mist': 'smog',
        'Fog': 'smog'
    }
    return icons.get(condition, 'cloud')

def fetch_weather_data():
    """Fetch fresh weather data from the API"""
    OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    
    if not API_KEY:
        raise ValueError("OpenWeather API key not found. Please set OPENWEATHER_API_KEY in your .env file.")

    parameters = {
        "lat": 1.2966,  # NUS Kent Ridge campus coordinates
        "lon": 103.7764,
        "appid": API_KEY,
        "units": "metric"  # Use metric units for temperature
    }

    response = requests.get(OWM_Endpoint, params=parameters)
    response.raise_for_status()
    data = response.json()

    formatted_data = {}
    for item in data["list"]:
        # Get date and time
        dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
        date = dt.strftime("%b %d")  # Format: "May 27"
        
        # Get weather details
        weather_condition = item["weather"][0]["main"]
        temp = round(item["main"]["temp"])  # Temperature is already in Celsius
        
        # Create forecast object
        forecast = {
            "time": dt.strftime("%H:%M"),
            "description": weather_condition,
            "temp": temp,
            "icon": get_weather_icon(weather_condition)
        }
        
        # Add to formatted data
        if date not in formatted_data:
            formatted_data[date] = []
        formatted_data[date].append(forecast)
    
    return formatted_data

def update_weather():
    """Update the cached weather data"""
    global cached_weather_data, last_update_time
    try:
        cached_weather_data = fetch_weather_data()
        sgt = pytz.timezone('Asia/Singapore')
        last_update_time = datetime.now(sgt)
        print(f"Weather data updated at {last_update_time.strftime('%Y-%m-%d %H:%M:%S SGT')}")
    except Exception as e:
        print(f"Error updating weather data: {e}")

def get_weather():
    """Get weather data from cache or fetch new data if needed"""
    global cached_weather_data
    if cached_weather_data is None:
        update_weather()
    return cached_weather_data

get_weather()




