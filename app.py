from flask import Flask, render_template, url_for, jsonify
from flask_apscheduler import APScheduler
from weather import get_weather, update_weather
from motivation import get_daily_quote
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')
scheduler = APScheduler()

# Scheduler configuration
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Singapore"

app.config.from_object(Config())

# Initialize scheduler
scheduler.init_app(app)
scheduler.start()

# Schedule weather update every 3 hours
@scheduler.task('interval', id='update_weather', hours=3, misfire_grace_time=900)
def scheduled_weather_update():
    update_weather()
    print(f"Scheduled weather update completed at {datetime.now()}")

@app.route('/')
def index():
    weather_data = get_weather()
    # Get current time in SGT
    sgt = pytz.timezone('Asia/Singapore')
    last_update = datetime.now(sgt).strftime("%H:%M:%S SGT")
    daily_quote = get_daily_quote()
    return render_template('index.html', 
                         weather_data=weather_data, 
                         last_update=last_update,
                         daily_quote=daily_quote)

@app.route('/refresh-weather')
def refresh_weather():
    update_weather()
    weather_data = get_weather()
    # Get current time in SGT
    sgt = pytz.timezone('Asia/Singapore')
    last_update = datetime.now(sgt).strftime("%H:%M:%S SGT")
    return jsonify({
        'weather_data': weather_data,
        'last_update': last_update
    })

# Vercel requires this
app.debug = True

if __name__ == '__main__':
    # Initial weather update
    update_weather()
    app.run(host='0.0.0.0', port=8000) 