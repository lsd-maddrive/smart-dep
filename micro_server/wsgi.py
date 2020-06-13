import logging
import os

from flask import Flask, request
from flask_restplus import Api
from flask_cors import CORS

from api_v1 import api as ns
from database import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    api = Api(app)
    api.add_namespace(ns)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config['FLASK_DEBUG'] = os.getenv('API_SERVER_DEBUG', True)
    app.config['TESTING'] = os.getenv('API_SERVER_TESTING', False)

    db_uri = os.getenv('DB_URI')
    if db_uri is None:
        logger.critical(f"DB URI IS NOT FOUND!")
        sys.exit(1)

    app.config['DATABASE_URI'] = db_uri
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    logger.debug(f"DB URI is set to {db_uri}.")

    # Must be initialized after SQLALCHEMY_DATABASE_URI set
    db.init_app(app)

    rabbitmq_uri = os.getenv('RABBITMQ_URI')
    if rabbitmq_uri is None:
        logger.critical(f"RABBITMQ URI IS NOT FOUND!")
        sys.exit(1)

    app.config['RABBITMQ_URI'] = rabbitmq_uri
    logger.debug(f"RABBITMQ URI is set to {rabbitmq_uri}")

    return app