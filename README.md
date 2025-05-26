# NUS Weather Forecast

A beautiful weather forecast application for the NUS Kent Ridge campus area. The application shows a 5-day weather forecast with temperature and weather conditions in an elegant, modern UI.

🌐 **Live Demo**: [View the application on Vercel](https://weather-forecast-raiaaa17.vercel.app)

## Features

- 5-day weather forecast for NUS Kent Ridge campus
- Real-time weather data from OpenWeatherMap API
- Automatic updates every 3 hours
- Modern, responsive design with animations
- Temperature in Celsius
- Weather condition icons
- Mobile-friendly interface
- Dark mode UI with glassmorphism effects

## Tech Stack

- Python 3.x
- Flask
- Flask-APScheduler
- OpenWeatherMap API
- HTML5
- CSS3
- Font Awesome icons
- Vercel (Deployment)

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Raiaaa17/Weather-Forecast.git
cd Weather-Forecast
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

5. Open your browser and navigate to `http://localhost:8000`

## Deployment

This application is deployed on Vercel. To deploy your own instance:

1. Fork this repository
2. Sign up for a [Vercel account](https://vercel.com)
3. Create a new project and import your forked repository
4. Add your environment variables in Vercel:
   - `OPENWEATHERMAP_API_KEY`: Your OpenWeatherMap API key
5. Deploy!

## Project Structure

```
Weather-Forecast/
├── app.py              # Flask application
├── weather.py          # Weather API integration
├── requirements.txt    # Project dependencies
├── vercel.json        # Vercel configuration
├── .env               # Environment variables (not tracked by Git)
├── static/
│   └── css/
│       └── style.css  # Styles
└── templates/
    └── index.html     # Main template
```

## Environment Variables

The application requires the following environment variables:
- `OPENWEATHERMAP_API_KEY` - Your OpenWeatherMap API key

⚠️ **Important**: Never commit your `.env` file or expose your API keys. The `.env` file is already added to `.gitignore`.

## Contact

- **Developer**: Rayana Diana
- **Email**: rayanarahadiva@gmail.com
- **GitHub**: [@Raiaaa17](https://github.com/Raiaaa17)

## Contributing

Feel free to open issues and pull requests!

## License

This project is open source and available under the [MIT License](LICENSE). 