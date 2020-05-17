import json
import os
import random
import time
from threading import Thread, Event

from flask import Flask, request
# >>???Why Resource, Resource, fields. What for? Not used..
from flask_restplus import Resource, Namespace, Api, fields
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from sockets import socketio
from api_v1 import api as ns

# if remove app inside main function - ERROR. 
app = Flask(__name__)

def main():
    ####### APP CONFIGURATION ZONE #######
    ########## OPTIONAL CONFIGS ##########
    app_debug_mode = os.getenv('API_SERVER_DEBUG')
    if app_debug_mode is None:
        logger.warning(f"API SERVER DEBUG is not found. DEFAULT DEBUG MODE is ENABLE")
        app.config['DEBUG'] = True 
    else:
        logger.debug(f"API SERVER DEBUG MODE is {'ENABLE' if app_debug_mode else 'DISABLE'}")
        app.config['DEBUG'] = app_debug_mode
    
    app_testing_mode = os.getenv('API_SERVER_TESTING')
    if app_testing_mode is None:
        app.config['TESTING'] = False 
        logger.warning(f"API SERVER TESTING is not found. DEFAULT TESTING MODE is DISABLE")
    else:
        app.config['TESTING'] = app_testing_mode
        logger.debug(f"API SERVER TESTING is {'ENABLE' if app_testing_mode else 'DISABLE'}")
    ########## MANDATORY CONFIGS ##########
    db_uri = os.getenv('DB_URI')
    if db_uri is None: 
        logger.critical(f"DB URI IS NOT FOUND!")   
        return 1 
    app.config['DATABASE_URI'] = db_uri
    logger.debug(f"DB URI is set to {db_uri}.")

    rabbitmq_uri = os.getenv('RABBITMQ_URI')
    if rabbitmq_uri is None:
        logger.critical(f"RABBITMQ URI IS NOT FOUND!")
        return 1
    app.config['RABBITMQ_URI'] = rabbitmq_uri
    logger.debug(f"RABBITMQ URI is set to {rabbitmq_uri}")

    # global db 
    # db = SQLAlchemy(metadata=metadata)
    # db.init_app(app)
    # logger.debug(f"CHECK db type: {type(db)}")

    # >>Initialization. Connect soketio and flask 
    socketio.init_app(app)
    api = Api(app)
    api.add_namespace(ns)
    # >>CORS = Cross Origin Resource Sharing
    # >>enable CORS for all domains on all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # >> start up web service, replaces app.run(...)
    socketio.run(app, debug=True, use_reloader=True)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())