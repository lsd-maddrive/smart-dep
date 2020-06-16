import logging
import os

from flask import Blueprint
from flask_restplus import Api
from flask_cors import CORS

from api_v1 import api as ns
from api_func import create_app
from sockets import socketio
from database import db

import messages as msgs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()
db.init_app(app)

if os.getenv('RECREATE_TABLES', False):
    with app.app_context():
        db.drop_all()
        db.create_all()

if os.getenv('PREPARE_RABBITMQ', False):
    msgs.init_broker(app.config['RABBITMQ_URI'])

socketio.init_app(app)

api = Api(app)
api.add_namespace(ns)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    socketio.run(app, debug=False, use_reloader=True)
