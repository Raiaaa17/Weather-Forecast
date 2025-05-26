# NUS Weather Forecast

A beautiful weather forecast application for the NUS Kent Ridge campus area. The application shows a 5-day weather forecast with temperature and weather conditions in an elegant, modern UI.

## Features

- 5-day weather forecast for NUS Kent Ridge campus
- Real-time weather data from OpenWeatherMap API
- Modern, responsive design with animations
- Temperature in Celsius
- Weather condition icons
- Mobile-friendly interface

## Tech Stack

- Python 3.x
- Flask
- OpenWeatherMap API
- HTML5
- CSS3
- Font Awesome icons

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd rain_alert
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
rain_alert/
├── app.py              # Flask application
├── weather.py          # Weather API integration
├── requirements.txt    # Project dependencies
├── static/
│   └── css/
│       └── style.css  # Styles
└── templates/
    └── index.html     # Main template
```

## Environment Variables

The application uses the following environment variables:
- `OPENWEATHERMAP_API_KEY` - Your OpenWeatherMap API key

## Contributing

Feel free to open issues and pull requests! 