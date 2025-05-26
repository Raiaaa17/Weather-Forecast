from flask import Flask, render_template, url_for, jsonify, make_response
from weather import get_weather, update_weather
from motivation import get_daily_quote
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    try:
        weather_data = get_weather()
        # Get current time in SGT
        sgt = pytz.timezone('Asia/Singapore')
        current_time = datetime.now(sgt)
        last_update = current_time.strftime("%H:%M:%S")
        
        # Get daily quote
        daily_quote = get_daily_quote()
        
        # Set cache control headers for the page
        response = make_response(render_template('index.html', 
                                               weather_data=weather_data, 
                                               last_update=last_update,
                                               daily_quote=daily_quote))
        # Cache for 5 minutes
        response.headers['Cache-Control'] = 'public, max-age=300'
        return response
    except Exception as e:
        return str(e), 500

@app.route('/refresh-weather')
def refresh_weather():
    try:
        # Get fresh data from the API
        weather_data = update_weather()
        
        # Get current time in SGT
        sgt = pytz.timezone('Asia/Singapore')
        current_time = datetime.now(sgt)
        last_update = current_time.strftime("%H:%M:%S")
        
        return jsonify({
            'weather_data': weather_data,
            'last_update': last_update
        })
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 