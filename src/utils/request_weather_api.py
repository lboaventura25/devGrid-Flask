import os
import requests as api


def request_weather_api(city_name: str):
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = os.environ.get('API_KEY')
    url_api = f'{base_url}?q={city_name}&appid={api_key}&units=metric'

    response = api.get(url_api, headers=headers).json()

    return response
