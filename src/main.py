from flask import Flask
from flask_cors import CORS

from settings import logger, load_configuration
from views.users import users_blueprint 


app = Flask(__name__)
app.register_blueprint(users_blueprint)

CORS(app, automatic_options=True)

if __name__ == '__main__':
    server_config = load_configuration()

    logger.info(f'Service configurations: {server_config}')
    logger.info('DevGrid service initialized and ready to use!\n')

    app.run(**server_config)
