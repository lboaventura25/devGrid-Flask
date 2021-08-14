from flask import Blueprint
from flask_cors import CORS

from controllers import users as users_controller

users_blueprint = Blueprint('user', __name__, url_prefix='/api')
CORS(users_blueprint)

@users_blueprint.route('/users/', methods=['GET', 'POST'])
def get_user():
    return "Hello World"
