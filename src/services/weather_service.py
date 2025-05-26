import requests
import json
import logging
from datetime import datetime
from src.config.settings import (
    OPENWEATHER_API_KEY,
    WEATHER_API_URL,
    WEATHER_COORDINATES,
    WEATHER_CACHE_FILE
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherService:
    WEATHER_ICONS = {
        'Clear': 'sun',
        'Clouds': 'cloud',
        'Rain': 'cloud-rain',
        'Snow': 'snowflake',
        'Thunderstorm': 'bolt',
        'Drizzle': 'cloud-rain',
        'Mist': 'smog',
        'Fog': 'smog'
    }

    @staticmethod
    def kelvin_to_celsius(kelvin):
        """Convert Kelvin to Celsius."""
        return round(kelvin - 273.15)

    @staticmethod
    def get_weather_icon(condition):
        """Get appropriate weather icon."""
        return WeatherService.WEATHER_ICONS.get(condition, 'cloud')

    @classmethod
    def format_weather_data(cls, raw_data):
        """Format raw weather data into structured format."""
        formatted_data = {}
        
        try:
            for item in raw_data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                time = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
                
                if date not in formatted_data:
                    formatted_data[date] = []
                
                weather_condition = item['weather'][0]['main']
                formatted_data[date].append({
                    'time': time,
                    'temp': cls.kelvin_to_celsius(item['main']['temp']),
                    'description': weather_condition,
                    'icon': cls.get_weather_icon(weather_condition)
                })
            
            logger.info("Weather data formatted successfully")
            return formatted_data
            
        except KeyError as e:
            logger.error(f"Missing key in weather data: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error formatting weather data: {e}")
            return {}

    @staticmethod
    def cache_weather(weather_data):
        """Cache weather data."""
        try:
            cache = {
                'timestamp': datetime.now().isoformat(),
                'data': weather_data
            }
            with open(WEATHER_CACHE_FILE, 'w') as f:
                json.dump(cache, f)
            logger.info("Weather data cached successfully")
        except Exception as e:
            logger.error(f"Error caching weather data: {e}")

    @staticmethod
    def get_cached_weather():
        """Get cached weather data if available."""
        try:
            with open(WEATHER_CACHE_FILE, 'r') as f:
                return json.load(f)['data']
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            logger.info("No valid weather cache found")
            return None
        except Exception as e:
            logger.error(f"Error reading weather cache: {e}")
            return None

    @classmethod
    def update_weather(cls):
        """Fetch new weather data from API."""
        if not OPENWEATHER_API_KEY:
            logger.error("OpenWeather API key not found")
            return None

        params = {
            'lat': WEATHER_COORDINATES['lat'],
            'lon': WEATHER_COORDINATES['lon'],
            'appid': OPENWEATHER_API_KEY
        }

        try:
            response = requests.get(WEATHER_API_URL, params=params, timeout=10)
            response.raise_for_status()
            
            weather_data = cls.format_weather_data(response.json())
            cls.cache_weather(weather_data)
            logger.info("Weather data updated successfully")
            return weather_data
            
        except requests.Timeout:
            logger.error("Weather API request timed out")
        except requests.RequestException as e:
            logger.error(f"Weather API request failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error updating weather: {e}")
        
        return cls.get_cached_weather() or {}

    @classmethod
    def get_weather(cls):
        """Get weather data from cache or update if needed."""
        cached_data = cls.get_cached_weather()
        if cached_data:
            return cached_data
        return cls.update_weather() 