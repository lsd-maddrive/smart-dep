import os

from kombu import Connection, Exchange

from flask_restplus import Api
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from api_server.api_v1 import api as ns
from api_server.api_func import create_app
from api_server.sockets import socketio
from api_server.database import db

app = create_app()

db.init_app(app)

if os.getenv('RECREATE_TABLES', False):
    with app.app_context():
        db.drop_all()
        db.create_all()

if os.getenv('PREPARE_RABBITMQ', False):
    with Connection(app.config['RABBITMQ_URI']) as conn:
        channel = conn.channel()
        device_exchange = Exchange('amq.topic', type='topic', durable=True)

        cmd_exchange = Exchange('commands', type='topic', durable=True)
        cmd_exchange.declare(channel=channel)
        device_exchange.bind_to(cmd_exchange, routing_key='cmd.*.*', channel=channel)

        cfg_exchange = Exchange('configurations', type='topic', durable=True)
        cfg_exchange.declare(channel=channel)
        device_exchange.bind_to(cfg_exchange, routing_key='cfg.*', channel=channel)

        state_exchange = Exchange('states', type='topic', durable=True)
        state_exchange.declare(channel=channel)
        state_exchange.bind_to(device_exchange, routing_key='state.*.*', channel=channel)

socketio.init_app(app)
api = Api(app)
api.add_namespace(ns)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    socketio.run(app, debug=False, use_reloader=True)