from flask import Flask, render_template, url_for, jsonify, make_response
from weather import get_weather, update_weather
from motivation import get_daily_quote
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

def get_next_update_time():
    """Calculate when the next weather update should occur"""
    sgt = pytz.timezone('Asia/Singapore')
    now = datetime.now(sgt)
    # Round to the next 3-hour mark
    hours = (now.hour // 3 + 1) * 3
    next_update = now.replace(hour=hours, minute=0, second=0, microsecond=0)
    if next_update < now:
        next_update += timedelta(days=1)
    return next_update

@app.route('/')
def index():
    try:
        weather_data = get_weather()
        # Get current time in SGT
        sgt = pytz.timezone('Asia/Singapore')
        current_time = datetime.now(sgt)
        last_update = current_time.strftime("%H:%M:%S SGT")
        
        # Calculate next update time
        next_update = get_next_update_time()
        next_update_str = next_update.strftime("%H:%M:%S SGT")
        
        # Get daily quote
        daily_quote = get_daily_quote()
        
        # Set cache control headers for the page
        response = make_response(render_template('index.html', 
                                               weather_data=weather_data, 
                                               last_update=last_update,
                                               next_update=next_update_str,
                                               daily_quote=daily_quote))
        # Cache for 5 minutes
        response.headers['Cache-Control'] = 'public, max-age=300'
        return response
    except Exception as e:
        return str(e), 500

@app.route('/refresh-weather')
def refresh_weather():
    try:
        update_weather()
        weather_data = get_weather()
        # Get current time in SGT
        sgt = pytz.timezone('Asia/Singapore')
        current_time = datetime.now(sgt)
        last_update = current_time.strftime("%H:%M:%S SGT")
        
        # Calculate next update time
        next_update = get_next_update_time()
        next_update_str = next_update.strftime("%H:%M:%S SGT")
        
        return jsonify({
            'weather_data': weather_data,
            'last_update': last_update,
            'next_update': next_update_str
        })
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 