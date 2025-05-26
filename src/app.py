from flask import Flask, render_template
from flask_apscheduler import APScheduler
from datetime import datetime
import logging

from src.config.settings import Config
from src.services.weather_service import WeatherService
from src.services.quote_service import QuoteService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATE_FOLDER)
    
    app.config.from_object(Config)
    
    # Initialize scheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    
    # Schedule weather updates
    @scheduler.task('interval', id='update_weather', hours=3, misfire_grace_time=900)
    def scheduled_weather_update():
        try:
            WeatherService.update_weather()
            logger.info(f"Scheduled weather update completed at {datetime.now()}")
        except Exception as e:
            logger.error(f"Scheduled weather update failed: {e}")
    
    scheduler.start()
    
    @app.route('/')
    def index():
        try:
            weather_data = WeatherService.get_weather()
            daily_quote = QuoteService.get_daily_quote()
            last_update = datetime.now().strftime("%H:%M:%S")
            
            return render_template('index.html',
                                weather_data=weather_data,
                                daily_quote=daily_quote,
                                last_update=last_update)
        except Exception as e:
            logger.error(f"Error rendering index page: {e}")
            return render_template('error.html', error=str(e))
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Initial weather update
    try:
        WeatherService.update_weather()
        logger.info("Initial weather update completed")
    except Exception as e:
        logger.error(f"Initial weather update failed: {e}")
    
    app.run(host='0.0.0.0', port=8000) 