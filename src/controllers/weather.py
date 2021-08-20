from datetime import datetime

from sqlalchemy.sql.functions import now
from database.models import Weather
from database import db
from utils.request_weather_api import request_weather_api
from utils.date_plus_five_minutes import date_plus_five_minutes


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

        created_date_plus_five_minutes = date_plus_five_minutes(created_date)
        current_time = datetime.now()

        if created_date_plus_five_minutes > current_time:
            return weather, code

    try:
        response = request_weather_api(city_name)
        status_response = int(response['cod'])

        if status_response == 404:
            return "Sorry. We couldn't find the specified city.", 404

        description = response['weather'][0]['description']
        temperature = response['main']['temp']

        if code == 200:
            new_weather = {
                'temperature': temperature,
                'description': description,
                'created_date': now()
            }

            weather, code = db.update(Weather, city_name, new_weather)
            return weather.to_dict(), code

        new_weather = Weather(
            city_name,
            temperature,
            description,
            datetime.now()
        )

        db.insert_one(new_weather)

        return new_weather.to_dict(), 200
    except:
        return 'Sorry. There was an error on server, try again later.', 500
