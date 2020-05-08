import json
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

app = Flask(__name__)
app.config.from_object('config')
# >>Flask-SocketIO gives Flask applications access to low latency
# >>bi-directional communications between the clients and the server. 
# >>Initialization. Connect soketio and flask 
socketio.init_app(app)
# >>The main entry point for the application:
# >>app = Flask(...) && api = Api(...)
api = Api(app)
# >>????get environmental variables from defined ns and 
# >>registers resources from namespace for current instance of api 
api.add_namespace(ns)
# >>CORS = Cross Origin Resource Sharing
# >>????different apps can use one resource together?? 
# >>enable CORS for all domains on all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
# >> start up web service, replaces app.run(...)
    socketio.run(app, debug=True, use_reloader=True)
