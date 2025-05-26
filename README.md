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

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenWeatherMap API key:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```
   - You can get an API key by signing up at [OpenWeatherMap](https://openweathermap.org/api)

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
rain_alert/
├── app.py              # Flask application
├── weather.py          # Weather API integration
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (not tracked by Git)
├── static/
│   └── css/
│       └── style.css  # Styles
└── templates/
    └── index.html     # Main template
```

## Environment Variables

The application requires the following environment variables in a `.env` file:
- `OPENWEATHERMAP_API_KEY` - Your OpenWeatherMap API key

⚠️ **Important**: Never commit your `.env` file or expose your API keys. The `.env` file is already added to `.gitignore`.

## Contributing

Feel free to open issues and pull requests! 