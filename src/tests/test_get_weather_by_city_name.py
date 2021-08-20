import datetime
from freezegun import freeze_time

from controllers.weather import get_weather_by_city_name


@freeze_time('2021-08-20 09:31:43')
def test_get_weather_by_city_name_create_in_less_than_5_minutes(mocker, mock_weather):
    mocker.patch(
        'controllers.weather.db.get_one', return_value=(mock_weather, 200)
    )
    mocker.patch(
        'controllers.weather.date_plus_five_minutes',
        return_value=datetime.datetime(2021, 8, 20, 9, 34, 40)
    )

    expected = mock_weather.to_dict()
    response, code = get_weather_by_city_name('paris')

    assert response == expected
    assert code == 200


@freeze_time('2021-08-20 09:36:44')
def test_get_weather_by_city_name_create_in_bigger_than_5_minutes(
    mocker,
    mock_weather,
    mock_return_weather_api,
    update_weather_mock,
):
    mocker.patch(
        'controllers.weather.db.get_one', return_value=(mock_weather, 200)
    )
    mocker.patch(
        'controllers.weather.date_plus_five_minutes',
        return_value=datetime.datetime(2021, 8, 20, 9, 31, 43)
    )
    mocker.patch(
        'controllers.weather.request_weather_api',
        return_value=mock_return_weather_api
    )
    mocker.patch(
        'controllers.weather.db.update',
        return_value=(update_weather_mock, 200)
    )

    expected = update_weather_mock.to_dict()
    response, code = get_weather_by_city_name('paris')

    assert response == expected
    assert code == 200


@freeze_time('2021-08-20 09:36:44')
def test_get_weather_by_city_name_error_weather_api(
    mocker,
    mock_weather,
    mock_return_weather_api_error,
):
    mocker.patch(
        'controllers.weather.db.get_one', return_value=(mock_weather, 200)
    )
    mocker.patch(
        'controllers.weather.date_plus_five_minutes',
        return_value=datetime.datetime(2021, 8, 20, 9, 31, 43)
    )
    mocker.patch(
        'controllers.weather.request_weather_api',
        return_value=mock_return_weather_api_error
    )

    expected = "Sorry. We couldn't find the specified city."
    response, code = get_weather_by_city_name('paris')

    assert response == expected
    assert code == 404


@freeze_time('2021-08-20 09:36:44')
def test_get_weather_by_city_name_not_exist(
    mocker,
    mock_weather,
    mock_return_weather_api,
    mock_weather_from_api
):
    mocker.patch(
        'controllers.weather.db.get_one', return_value=(mock_weather, 404)
    )
    mocker.patch(
        'controllers.weather.date_plus_five_minutes',
        return_value=datetime.datetime(2021, 8, 20, 9, 31, 43)
    )
    mocker.patch(
        'controllers.weather.request_weather_api',
        return_value=mock_return_weather_api
    )

    expected = mock_weather_from_api.to_dict()
    response, code = get_weather_by_city_name('paris')

    assert response['description'] == expected['description']
    assert response['temperature'] == expected['temperature']
    assert response['city_name'] == expected['city_name']
    assert code == 200



@freeze_time('2021-08-20 09:36:44')
def test_get_weather_by_city_name_not_exist_exception(
    mocker,
    mock_weather,
):
    mocker.patch(
        'controllers.weather.db.get_one', return_value=(mock_weather, 404)
    )
    mocker.patch(
        'controllers.weather.date_plus_five_minutes',
        return_value=datetime.datetime(2021, 8, 20, 9, 31, 43)
    )
    mocker.patch(
        'controllers.weather.request_weather_api',
        return_value=Exception('Something went wrong')
    )

    expected = 'Sorry. There was an error on server, try again later.'
    response, code = get_weather_by_city_name('paris')

    assert response == expected
    assert code == 500
