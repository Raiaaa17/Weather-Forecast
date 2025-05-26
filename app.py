from flask import Flask, render_template, url_for
from weather import get_weather

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    weather_data = get_weather()
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True) 