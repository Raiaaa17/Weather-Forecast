import requests
from datetime import datetime

def get_weather():
    OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    API_KEY = "ebd23d6d15dc62fec33baa419e78fb6c"

    parameters = {
        "lat": 1.2966,  # NUS Kent Ridge campus coordinates
        "lon": 103.7764,
        "appid": API_KEY,
        "units": "metric"  # Add metric units for better temperature understanding
    }

    response = requests.get(OWM_Endpoint, params=parameters)
    response.raise_for_status()
    data = response.json()

    forecasts = data["list"]
    dic = {}
    for cast in forecasts:    
        weather = cast["weather"][0]["main"]
        temp = round(cast["main"]["temp"])  # Get temperature
        dt = datetime.strptime(cast["dt_txt"], "%Y-%m-%d %H:%M:%S")
        formatted_date = dt.strftime("%b %d")
        formatted_time = dt.strftime("%H.%M")

        if formatted_date not in dic:
            dic[formatted_date] = {}
        if formatted_time not in dic[formatted_date]:
            dic[formatted_date][formatted_time] = []
        dic[formatted_date][formatted_time].extend([weather, temp])  # Add temperature to the data
        
    return dic

get_weather()




