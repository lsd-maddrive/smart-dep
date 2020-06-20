import logging
import os

from flask import Blueprint
from flask_restplus import Api
from flask_cors import CORS

from api_v1 import api as ns
from api_func import create_app
from sockets import socketio
from database import db, create_place


import messages as msgs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()
db.init_app(app)

if os.getenv('RECREATE_TABLES', False):
    with app.app_context():
        logger.debug(f"RECREATE TABLES")
        db.drop_all()
        db.create_all()
        place_info = {
            'name': 'KEMZ', 
            'num': '8201',
            'attr_os': ['Linux'], 
            'attr_software': ['Matlab'], 
            'attr_people': 25,
            'attr_computers': 10, 
            'attr_board': True, 
            'attr_projector': True
        }
        place = create_place(place_info)
        db.session.add(place)
        db.session.commit()


if os.getenv('PREPARE_RABBITMQ', False):
    msgs.init_broker(app.config['RABBITMQ_URI'])

socketio.init_app(app)

api = Api(app)
api.add_namespace(ns)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    socketio.run(app, debug=False, use_reloader=True)
