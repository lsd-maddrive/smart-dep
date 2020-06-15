import logging
import os

from flask import Blueprint
from flask_restplus import Api
from flask_cors import CORS

from api_server.api_v1 import api as ns 
from api_server.api_func import create_app
from api_server.sockets import socketio
from api_server.database import db, load_user 


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()
db.init_app(app)

socketio.init_app(app)

api = Api(app)
api.add_namespace(ns)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    socketio.run(app, debug=False, use_reloader=True)