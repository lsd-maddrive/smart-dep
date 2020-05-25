import os
import sys 
sys.path.append("..")

from flask import Flask, request
from flask_restplus import Api
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from api_server.api_v1 import api as ns 
from api_server.sockets import socketio
from db.database import db 
from db.database import * 

def create_app(test_config=False):
    app = Flask(__name__)
    # if not test_config:
    #     app.config['FLASK_DEBUG'] = os.getenv('API_SERVER_DEBUG', True)
    #     app.config['TESTING'] = os.getenv('API_SERVER_TESTING', False)

    #     db_uri = os.getenv('DB_URI')
    #     if db_uri is None: 
    #         logger.critical(f"DB URI IS NOT FOUND!")   
    #         sys.exit(1)
    #         # ????????????
    #         return 1

    #     app.config['DATABASE_URI'] = db_uri
    #     app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    #     logger.debug(f"DB URI is set to {db_uri}.")

    #     rabbitmq_uri = os.getenv('RABBITMQ_URI')
    #     if rabbitmq_uri is None:
    #         logger.critical(f"RABBITMQ URI IS NOT FOUND!")
    #         sys.exit(1)
    #         # ????????????
    #         return 1

    #     app.config['RABBITMQ_URI'] = rabbitmq_uri
    #     logger.debug(f"RABBITMQ URI is set to {rabbitmq_uri}")

    #     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    return app 

app = create_app()

app.config['FLASK_DEBUG'] = os.getenv('API_SERVER_DEBUG', True)
app.config['TESTING'] = os.getenv('API_SERVER_TESTING', False)

db_uri = os.getenv('DB_URI')
if db_uri is None: 
    logger.critical(f"DB URI IS NOT FOUND!")   
    sys.exit(1)

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

db.init_app(app)

# >>Initialization. Connect soketio and flask 
socketio.init_app(app)
api = Api(app)
api.add_namespace(ns)
# >>CORS = Cross Origin Resource Sharing
# >>enable CORS for all domains on all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    socketio.run(app, debug=False, use_reloader=True)