import logging
import os
from flask import Flask

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app(test_config=False):
    app = Flask(__name__)
    if test_config == False:
        logger.debug('Usage of environmental configuration')
        app.config['FLASK_DEBUG'] = os.getenv('API_SERVER_DEBUG', True)
        app.config['TESTING'] = os.getenv('API_SERVER_TESTING', False)
        app.config['LOGIN_ENABLED'] = os.getenv('API_LOGIN_ENABLED', False)

        secret = os.getenv('API_SECRET_KEY')
        if secret is None:
            logger.critical(f"API SECRET KEY IS NOT FOUND")
            sys.exit(1)
        app.config['SECRET_KEY'] = secret

        db_uri = os.getenv('DB_URI')
        if db_uri is None:
            logger.critical(f"DB URI IS NOT FOUND!")
            sys.exit(1)

        # TODO: check if 2 configs for DB is needed?
        app.config['DATABASE_URI'] = db_uri
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        logger.debug(f"DB URI is set to {db_uri}.")

        rabbitmq_uri = os.getenv('RABBITMQ_URI')
        if rabbitmq_uri is None:
            logger.critical(f"RABBITMQ URI IS NOT FOUND!")
            sys.exit(1)

        app.config['RABBITMQ_URI'] = rabbitmq_uri
        logger.debug(f"RABBITMQ URI is set to {rabbitmq_uri}")

        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    return app