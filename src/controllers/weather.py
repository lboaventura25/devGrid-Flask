from datetime import datetime, timedelta
import os
import requests as api
from database.models import Weather
from database import db


def get_all_weathers(max_number: int) -> tuple:
    result, code = db.get_all(Weather, max_number)

    if code == 200:
        weathers = [weather.to_dict() for weather in result]
        return weathers, code

    return result, code


def get_weather_by_city_name(city_name: str) -> tuple:
    result, code = db.get_one(Weather, city_name)

    if code == 200:
        weather = result.to_dict()

        created_date = weather['created_date']

        created_date_plus_five_minutes = created_date + timedelta(minutes=5)
        current_time = datetime.now()

        if created_date_plus_five_minutes > current_time:
            return weather, code
        
        db.delete(Weather, city_name)


    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = os.environ.get('API_KEY')
    url_api = f'{base_url}?q={city_name}&appid={api_key}&units=metric'

    response = api.get(url_api, headers=headers).json()

    status_response = int(response['cod'])

    if status_response == 404:
        return "Sorry. We couldn't find the specified city.", 404

    description = response['weather'][0]['description']
    temperature = response['main']['temp']

    weather = Weather(
        city_name,
        temperature,
        description
    )

    db.insert_one(weather)

    return weather.to_dict(), 200
