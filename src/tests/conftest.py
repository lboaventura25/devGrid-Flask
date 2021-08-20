import pytest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database.models import Weather


@pytest.fixture
def flask_app_mock():
    app_mock = Flask(__name__)

    app_mock.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory'
    app_mock.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db = SQLAlchemy(app_mock)
    db.init_app(app_mock)
    return app_mock


@pytest.fixture
def mock_weather():
    weather = Weather(
        city_name='paris',
        description='clean sky',
        temperature=13.18,
        created_date='2021-08-20 09:31:43'
    )

    return weather


@pytest.fixture
def mock_weather_bigger_than_5_minutes():
    weather = Weather(
        city_name='paris',
        description='clean sky',
        temperature=13.18,
        created_date='2021-08-20 09:30:43'
    )

    return weather


@pytest.fixture
def mock_weather_from_api():
    weather = Weather(
        city_name='paris',
        description='clear sky',
        temperature='14.59',
        created_date='2021-08-20 09:36:44'
    )

    return weather


@pytest.fixture
def update_weather_mock():
    weather = Weather(
        city_name='paris',
        description='clear sky',
        temperature=14.59,
        created_date='2021-08-20 09:31:43'
    )

    return weather


@pytest.fixture
def mock_return_weather_api():
    weather = {
        "weather": [
            {
            "description": "clear sky",
            }
        ],
        "main": {
            "temp": 14.59,
        },
        "cod": 200
    }

    return weather


@pytest.fixture
def mock_return_weather_api_error():
    weather = {
        "cod": "404",
        "message": "city not found"
    }

    return weather

@pytest.fixture
def mock_weather_list_object():
    weathers = []
    cities = ['paris', 'lisboa', 'brasilia', 'maceio', 'orlando', 'monaco']

    for city in cities:
        weather = Weather(
            city_name=city,
            description='clean sky',
            temperature=13.18
        )
        weathers.append(weather)

    return weathers

@pytest.fixture
def mock_get_sqlalchemy(mocker):
    mock = mocker.patch('flask_sqlalchemy._QueryProperty.__get__')
    mock.return_value = mocker.Mock()

    return mock
