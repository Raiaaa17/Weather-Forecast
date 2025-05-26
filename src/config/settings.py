import os
from datetime import timedelta

# Flask Configuration
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Singapore"
    DEBUG = True
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

# API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
WEATHER_COORDINATES = {
    'lat': 1.2966,  # NUS Kent Ridge latitude
    'lon': 103.7764  # NUS Kent Ridge longitude
}

# Quotes Configuration
ZENQUOTES_API_URL = 'https://zenquotes.io/api/today'
QUOTE_CACHE_FILE = 'data/quote_cache.json'

# Update Intervals
WEATHER_UPDATE_INTERVAL = timedelta(hours=3)
QUOTE_UPDATE_INTERVAL = timedelta(days=1)

# Cache Configuration
CACHE_DIR = 'data'
WEATHER_CACHE_FILE = os.path.join(CACHE_DIR, 'weather_cache.json')

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True) 