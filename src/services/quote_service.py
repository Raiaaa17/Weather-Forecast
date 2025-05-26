import requests
import json
import logging
from datetime import datetime
from src.config.settings import ZENQUOTES_API_URL, QUOTE_CACHE_FILE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuoteService:
    @staticmethod
    def get_cached_quote():
        """Retrieve cached quote if it exists and is from today."""
        try:
            with open(QUOTE_CACHE_FILE, 'r') as f:
                cache = json.load(f)
                if cache.get('date') == datetime.now().strftime('%Y-%m-%d'):
                    logger.info("Retrieved quote from cache")
                    return cache.get('quote')
        except FileNotFoundError:
            logger.info("No cache file found")
        except json.JSONDecodeError:
            logger.error("Invalid cache file format")
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
        return None

    @staticmethod
    def cache_quote(quote_data):
        """Cache the quote with current date."""
        try:
            cache = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'quote': quote_data
            }
            with open(QUOTE_CACHE_FILE, 'w') as f:
                json.dump(cache, f)
            logger.info("Quote cached successfully")
        except Exception as e:
            logger.error(f"Error caching quote: {e}")

    @classmethod
    def get_daily_quote(cls):
        """Get daily quote from cache or API."""
        # Try to get cached quote first
        cached_quote = cls.get_cached_quote()
        if cached_quote:
            return cached_quote

        try:
            response = requests.get(ZENQUOTES_API_URL, timeout=5)
            response.raise_for_status()  # Raise exception for bad status codes
            
            data = response.json()
            if data and len(data) > 0:
                quote_data = {
                    'content': data[0]['q'],
                    'author': data[0]['a']
                }
                cls.cache_quote(quote_data)
                logger.info("Retrieved new quote from API")
                return quote_data
            
        except requests.Timeout:
            logger.error("API request timed out")
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
        except (KeyError, IndexError) as e:
            logger.error(f"Invalid API response format: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        # Fallback quotes for different error scenarios
        fallback_quotes = [
            {"content": "Every day is a new beginning.", "author": "Anonymous"},
            {"content": "Make each day count.", "author": "Anonymous"},
            {"content": "Stay positive, work hard, make it happen.", "author": "Anonymous"}
        ]
        
        from random import choice
        fallback = choice(fallback_quotes)
        logger.info("Using fallback quote")
        return fallback 