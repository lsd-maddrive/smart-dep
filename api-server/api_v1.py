import json
import random
import time
from threading import Thread, Event
import sys 
sys.path.append("..")

from kombu import Connection, Exchange, Producer

from flask import request, current_app
from flask_restplus import Resource, Namespace, fields
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import metadata, Commands, Configs, States

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api = Namespace('api/v1', description="Main API namespace")
# >>allows you to instantiate and register models to your API or Namespace.
# >>???What does it mean "register models to your API"
_model_state = api.model('State', {
    'device_id': fields.String,
    'type': fields.String
})
# >>Polymorphism
# >> Nested for dicts, lists 
_model_light = api.inherit('Light', _model_state, {
    'state': fields.Nested(api.model('LightState', {
        'enabled': fields.Boolean
    })
    ),
})

_model_power = api.inherit('Power', _model_state, {
    'state': fields.Nested(api.model('PowerState', {
        'enabled': fields.Boolean
    })
    ),
})

_powers_db = [
    {
        'device_id': '0',
        'type': 'power',
        'state': {
            'enabled': True
        }
    },
    {
        'device_id': '1',
        'type': 'power',
        'state': {
            'enabled': False
        }
    },
]

db_uri = os.getenv('DB_URI')
if db_uri is None:
    logger.critical('DB URI IS NOT FOUND')
else:
    engine = current_app(db_uri)
    session = Session(engine)
    logger.debug("DB session is created successfully!")


@api.route('/place/<string:place_id>/powers', endpoint='powers')
@api.param('place_id', 'ID of place')
class PowerUnits(Resource):
    @api.marshal_with(_model_power, as_list=True)
    def get(self, place_id):
        if current_app.debug:
            return _powers_db
        else:
            # TODO - db request required
            query = session.query(States).filter(States.place_id.like(place_id))
            print(query)
            return {}
# >>The decorator marshal_with() is what actually takes your data object
# >>and applies the field filtering

_lights_db = [
    {
        'device_id': '0',
        'type': 'light',
        'state': {
            'enabled': True
        }
    }
]


@api.route('/place/<string:place_id>/lights', endpoint='lights')
@api.param('place_id', 'ID of place')
class LightUnits(Resource):
    @api.marshal_with(_model_light, as_list=True)
    def get(self, place_id):
        if current_app.debug:
            return _lights_db
        else:
            # TODO - db request required
            return {}


@api.route('/cmd/<string:place_id>', endpoint='command')
@api.param('place_id', 'ID of place')
class CommandResender(Resource):
    def post(self, place_id):
        data = request.get_json()
        logger.debug(f'Received command: {data}')

        uri = current_app.config['RABBITMQ_URI']
        logger.debug(f"Connect to RabbitMQ {uri}")
        conn = Connection(uri)
        logger.debug('>>>>Connection received!')
        channel = conn.channel()
        exchange = Exchange('commands', type='topic', durable=True)

        place_id = data['place_id']
        type_ = data['type']
        routing_key = f'cmd.{place_id}.{type_}'
        # TODO - Message update
        message = json.dumps(data)

        producer = Producer(exchange=exchange,
                            channel=channel, routing_key=routing_key)
        producer.publish(message)
        return f'Message sent: {message}'


_place_db = [
    {
        'id': '8201',
        'name': "KEMZ",
    }
]


_model_place = api.model('Place', {
    'id': fields.String,
    'name': fields.String,
})


@api.route('/place', endpoint='place')
class Places(Resource):
    @api.marshal_with(_model_place, as_list=True)
    def get(self):
        if current_app.debug:
            return _place_db
        else:
            # TODO - db request required
            return {}
