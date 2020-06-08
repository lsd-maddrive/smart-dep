from datetime import date, datetime, timedelta
import json
import logging
import os

from flask import request, current_app, flash, redirect, url_for
from flask_login import current_user, login_user
from flask_restplus import Resource, Namespace, fields
from kombu import Connection, Exchange, Producer
from pprint import pformat

import api_server.database as asdb 


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

time_delta = timedelta(minutes=int(os.getenv('DMINUTES', '5')))

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



# def json_serial(obj):
#     """
#       JSON serializer for objects not serializable by default json code
#       in case if we decide to get timestamp from DB as well 
#     """
#     if isinstance(obj, (datetime, date)):
#         return obj.isoformat()
#     raise TypeError ("Type %s not serializable" % type(obj))

@api.route('/place/<string:place_id>/powers', endpoint='powers')
@api.param('place_id', 'ID of place')
class PowerUnits(Resource):
    @api.marshal_with(_model_power, as_list=True)
    def get(self, place_id):
        if current_app.debug:
            return _powers_db
        else:
            with current_app.app_context():
                current_timestamp = datetime.now()
                check_time = current_timestamp - time_delta

                query = asdb.get_last_states(
                    check_time, place_id, 'power'
                )
                
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

                logger.debug(f"POWER LAST STATES:\n{pformat(powers_dict_list)}")
                
            return powers_dict_list


@api.route('/place/<string:place_id>/lights', endpoint='lights')
@api.param('place_id', 'ID of place')
class LightUnits(Resource):
    @api.marshal_with(_model_light, as_list=True)
    def get(self, place_id):
        if current_app.debug:
            return _lights_db
        else:
            current_timestamp = datetime.now()
            check_time = current_timestamp - time_delta

            query = asdb.get_last_states(
                check_time, place_id, 'light'
            )
        
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

            logger.debug(f"LIGHT LAST STATES:\n{pformat(lights_dict_list)}")
            
            return lights_dict_list


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
            current_timestamp = datetime.now()
            check_time = current_timestamp - time_delta

            query = asdb.get_last_places(check_time)
            
            places_dict_list = []

            for q in query:
                places_dict_list.append(
                    {
                        'id': q.place_id,
                        'name': q.place_id
                    }
                )
            
            logger.debug(f"PLACES LAST DATA:\n{pformat(places_dict_list)}")
            
            return places_dict_list


@api.route('/login', methods=['GET', 'POST'])
class Login(Resource):
    # if current_user.is_authenticated:
    #     logger.debug("Inside IF")
    # else:
    #     logger.debug("Else branch")
#         # if user is already registered 
#         # redirect person somewhere else 
#         # return redirect(url_for('index'))
#         # TODO: add url for redirecting
#         return 
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = asdb.get_user_data(form.username.data)
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         # TODO: add url for redirecting
#         # return redirect(url_for('index'))
#         return 
    pass