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
from api_server.api_func import create_app
from api_server.sockets import socketio
from database import db 
# from db.database import * 

app = create_app()

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