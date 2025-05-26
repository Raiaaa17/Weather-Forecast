import requests
import json
from datetime import datetime
import os

QUOTE_CACHE_FILE = 'quote_cache.json'
ZEN_QUOTES_API = 'https://zenquotes.io/api/today'

def get_cached_quote():
    try:
        if os.path.exists(QUOTE_CACHE_FILE):
            with open(QUOTE_CACHE_FILE, 'r') as f:
                cache = json.load(f)
                # Check if the quote is from today
                if cache.get('date') == datetime.now().strftime('%Y-%m-%d'):
                    return cache.get('quote')
    except Exception as e:
        print(f"Error reading cache: {e}")
    return None

def cache_quote(quote_data):
    try:
        cache = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'quote': quote_data
        }
        with open(QUOTE_CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"Error caching quote: {e}")

def get_daily_quote():
    # First check cache
    cached_quote = get_cached_quote()
    if cached_quote:
        return cached_quote

    try:
        response = requests.get(ZEN_QUOTES_API)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                quote_data = {
                    'content': data[0]['q'],
                    'author': data[0]['a']
                }
                # Cache the new quote
                cache_quote(quote_data)
                return quote_data
    except Exception as e:
        print(f"Error fetching quote: {e}")
    
    # Fallback quote if API fails
    return {
        'content': "Every day is a new beginning.",
        'author': "Anonymous"
    } 