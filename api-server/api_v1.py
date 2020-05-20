from datetime import date, datetime, timedelta
import json
import os
import random
import time
from threading import Thread, Event

from kombu import Connection, Exchange, Producer

from flask import request, current_app
from flask_restplus import Resource, Namespace, fields
import logging
from pprint import pformat
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from models import metadata, Commands, Configs, States

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api = Namespace('api/v1', description="Main API namespace")

_model_state = api.model('State', {
    'device_id': fields.String,
    'type': fields.String
})

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

# _powers_db = [
#     {
#         'device_id': '0',
#         'type': 'power',
#         'state': {
#             'enabled': True
#         }
#     },
#     {
#         'device_id': '1',
#         'type': 'power',
#         'state': {
#             'enabled': False
#         }
#     },
# ]

minutes = os.getenv('DMINUTES')
if minutes is None:
    time_delta = timedelta(minutes=5)
    logger.warning(f"DMINUTES is NOT FOUND! DEFAULT DMINUTES value is used 5 mins.")
else:
    time_delta = timedelta(minutes=int(minutes))
    logger.debug(f"DMINUTES is found. The value of delta time for DB is {minutes}")

db_uri = os.getenv('DB_URI')

if db_uri is None:
    logger.critical('DB URI IS NOT FOUND')
else:
    engine = create_engine(db_uri)
    session = Session(engine)
    logger.debug(f"DB session is created successfully! {db_uri}")


@api.route('/place/<string:place_id>/powers', endpoint='powers')
@api.param('place_id', 'ID of place')
class PowerUnits(Resource):
    @api.marshal_with(_model_power, as_list=True)
    def get(self, place_id):
        if current_app.debug:

            current_timestamp = datetime.now()
            check_time = current_timestamp - time_delta

            query = session.query(States). \
                    filter(States.timestamp >= check_time). \
                    filter(States.place_id == place_id). \
                    filter(States.type == 'power'). \
                    order_by(States.device_id, States.timestamp.desc()). \
                    distinct(States.device_id)
        
            powers_dict_list = [] 
            for q in query:
                powers_dict_list.append(
                    {
                        'device_id': q.device_id, 
                        'type': q.type, 
                        'state': q.state, 
                        # 'timestamp': json.dumps(q.timestamp, default=json_serial), 
                        # 'place_id': place_id
                    }
                )

            logger.debug(f"POWER UNIT DATA:\n{pformat(powers_dict_list)}")
            
            return powers_dict_list
        else:
            # TODO - db request required
            return {}
# >>The decorator marshal_with() is what actually takes your data object
# >>and applies the field filtering

# _lights_db = [
#     {
#         'device_id': '0',
#         'type': 'light',
#         'state': {
#             'enabled': True
#         }
#     }
# ]


# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code"""
#     if isinstance(obj, (datetime, date)):
#         return obj.isoformat()
#     raise TypeError ("Type %s not serializable" % type(obj))

@api.route('/place/<string:place_id>/lights', endpoint='lights')
@api.param('place_id', 'ID of place')
class LightUnits(Resource):
    @api.marshal_with(_model_light, as_list=True)
    def get(self, place_id):
        if current_app.debug:
            current_timestamp = datetime.now()
            check_time = current_timestamp - time_delta

            query = session.query(States). \
                    filter(States.timestamp >= check_time). \
                    filter(States.place_id == place_id). \
                    filter(States.type == 'light'). \
                    order_by(States.device_id, States.timestamp.desc()). \
                    distinct(States.device_id)
        
            lights_dict_list = [] 
            for q in query:
                lights_dict_list.append(
                    {
                        'device_id': q.device_id, 
                        'type': q.type, 
                        'state': q.state, 
                        # 'timestamp': json.dumps(q.timestamp, default=json_serial), 
                        # 'place_id': place_id
                    }
                )

            logger.debug(f"LIGHT UNIT DATA:\n{pformat(lights_dict_list)}")
            
            return lights_dict_list
        else:
            # TODO - db request required
            return {}


@api.route('/cmd/<string:place_id>', endpoint='command')
@api.param('place_id', 'ID of place')
class CommandResender(Resource):
    def post(self, place_id):
        logger.debug('COMMAND RESENDER HERE')
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


# _place_db = [
#     {
#         'id': '8201',
#         'name': "KEMZ",
#     }
# ]


_model_place = api.model('Place', {
    'id': fields.String,
    'name': fields.String,
})


@api.route('/place', endpoint='place')
class Places(Resource):
    @api.marshal_with(_model_place, as_list=True)
    def get(self):
        if current_app.debug:
            current_timestamp = datetime.now()
            check_time = current_timestamp - time_delta

            query = session.query(States.place_id). \
                    filter(States.timestamp < check_time). \
                    order_by(States.place_id, States.timestamp.desc()). \
                    distinct(States.place_id)
            
            places_dict_list = []

            for q in query:
                places_dict_list.append(
                    {
                        'id': q.place_id,
                        'name': q.place_id
                    }
                )
            
            logger.debug(f"Places UNIT DATA:\n{pformat(places_dict_list)}")
            
            return places_dict_list
        else:
            # TODO - db request required
            return {}
