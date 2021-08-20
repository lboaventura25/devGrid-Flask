from flask import Blueprint, request
from flask_cors import CORS

from controllers import weather as controller
from utils.formatters import create_response


weathers_blueprint = Blueprint('weather', __name__, url_prefix='/api')
CORS(weathers_blueprint)


@weathers_blueprint.route('/weather', methods=['GET'])
def get_weathers():
    max_number = int(request.args.get('max', 5))

    response, status = controller.get_all_weathers(max_number)

    return create_response(response, status)


@weathers_blueprint.route('/weather/<city_name>', methods=['GET'])
def get_weather_by_city_name(city_name: str):
    response, status = controller.get_weather_by_city_name(city_name)

    return create_response(response, status)
