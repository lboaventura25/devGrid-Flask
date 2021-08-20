from controllers.weather import get_all_weathers


def test_get_all_weathers(mocker, mock_weather_list_object):
    mocker.patch(
        'controllers.weather.db.get_all', return_value=(mock_weather_list_object, 200))
    
    expected = [weather.to_dict() for weather in mock_weather_list_object]
    response, code = get_all_weathers(5)

    assert response == expected
    assert code == 200
    assert len(response) == len(expected)


def test_get_all_weathers_error(mocker):
    mocker.patch(
        'controllers.weather.db.get_all', return_value=('Something went wrong', 500))
    
    expected = 'Something went wrong'
    response, code = get_all_weathers(2)

    assert response == expected
    assert code == 500
