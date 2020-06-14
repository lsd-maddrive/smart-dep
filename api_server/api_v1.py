from datetime import date, datetime, timedelta
import json
import logging
import os

from flask import request, current_app
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

                logger.debug(
                    f"POWER LAST STATES:\n{pformat(powers_dict_list)}")

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


_model_place_get = api.model('Place_get', {
    'id': fields.Integer,
    'num': fields.String,
    'name': fields.String,
})

_model_place_new = api.model('Place_new', {
    'num': fields.String,
    'name': fields.String,
})

_model_place_del = api.model('Place_del', {
    'id': fields.Integer,
})


@api.route('/place', endpoint='places_CRUD')
class Places(Resource):
    @api.marshal_with(_model_place_get, as_list=True)
    def get(self):
        current_timestamp = datetime.now()
        check_time = current_timestamp - time_delta

        places = asdb.get_places()

        result_places = []
        for place in places:
            result_places.append({
                'id': place.id,
                'num': place.num,
                'name': place.name
            })

        logger.debug(f"Requested places:\n{pformat(places)}")

        return places

    @api.expect(_model_place_new, validate=True)
    def post(self):
        place_info = request.get_json()
        logger.debug(f"Requested to create place:\n{pformat(place_info)}")

        new_place = asdb.create_place(place_info)
        logger.debug(f'Created new place: {new_place}')

    @api.expect(_model_place_new, validate=True)
    def put(self):
        place_info = request.get_json()
        logger.debug(f"Requested to update place:\n{pformat(place_info)}")

        asdb.update_place(place_info)

    @api.expect(_model_place_del, validate=True)
    def delete(self):
        place_info = request.get_json()
        logger.debug(f"Requested to delete place:\n{pformat(place_info)}")

        asdb.delete_place(place_info)


@api.route('/cmd/<string:place_id>', endpoint='command')
@api.param('place_id', 'ID of place')
class CommandResender(Resource):
    def post(self, place_id):
        logger.debug('COMMAND RESENDER HERE')
        data = request.get_json()
        logger.debug(f'Received command: {data}')

        uri = current_app.config['RABBITMQ_URI']
        logger.debug(f"Connect to RabbitMQ {uri}")
        with Connection(uri) as conn:
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


_model_device_types = api.model('Device_types', {
    'id': fields.String,
    'name': fields.String,
    'desc': fields.String,
})


@api.route('/device/types', endpoint='device_types')
class DeviceTypes(Resource):
    @api.expect(_model_device_types, as_list=True)
    def get(self):
        types = [
            {
                'id': 1,
                'name': 'light',
                'desc': 'Освещение',
                'default_config': {
                    'period': 3
                }
            },
            {
                'id': 2,
                'name': 'power',
                'desc': 'Электричество',
                'default_config': {
                    'period': 3
                }
            },
            {
                'id': 3,
                'name': 'env',
                'desc': 'Окружение',
                'default_config': {
                    'period': 3
                }
            },
        ]

        return types


_model_device_new = api.model('Device_new', {
    'id': fields.String,
    'ip_addr': fields.String,
    'reg_ts': fields.String,
})


@api.route('/device/new', endpoint='new_devices')
class DevicesNew(Resource):
    @api.expect(_model_device_new, as_list=True)
    def get(self):
        devices = asdb.get_new_devices()

        result = []
        for dev in devices:
            result.append({
                'id': str(dev.id),
                'ip_addr': dev.ip_addr,
                'reg_ts': dev.register_date.timestamp()
            })

        logger.debug(f"Requested new devices:\n{pformat(result)}")

        return result


_model_device_get_in = api.model('Device_get_in', {
    'place_id': fields.String,
})

_model_device_get_out = api.model('Device_get_out', {
    'id': fields.String,
    'name': fields.String,
    'type': fields.String,
    'place_id': fields.String,
})

_model_device_upd = api.model('Device_upd', {
    'id': fields.String,
    'name': fields.String,
    'type': fields.String,
    'place_id': fields.Integer
    # 'config': fields.String,
})

_model_device_del = api.model('Device_del', {
    'id': fields.String,
})


@api.route('/device', endpoint='device_RUD')
class Device(Resource):
    # @api.expect(_model_device_get_in)
    # @api.marshal_with(_model_device_get_out, as_list=True)
    def get(self):
        place_id = request.args.get('place_id')
        logger.debug(f"Requested devices for place: {place_id}")

        devices = asdb.get_devices(place_id)

        result = []
        for dev in devices:
            result.append({
                'id': str(dev.id),
                'name': dev.name,
                'type': dev.type,
                'place_id': dev.place_id,
                'config': dev.config,
            })

        logger.debug(f"Requested devices: {result}")

        return result

    @api.expect(_model_device_upd, validate=True)
    def put(self):
        device_info = request.get_json()
        logger.debug(f"Requested to update device:\n{pformat(device_info)}")

        asdb.update_device(device_info)

        uri = current_app.config['RABBITMQ_URI']
        logger.debug(f"Connect to RabbitMQ {uri}")
        with Connection(uri) as conn:
            exchange = Exchange('configurations', type='topic', durable=True)
            producer = Producer(exchange=exchange,
                                channel=conn.channel(),
                                routing_key=f'cfg.reset')

            message = json.dumps({
                'device_id': device_info['id']
            })
            producer.publish(message)
        return 200


    @api.expect(_model_device_del, validate=True)
    def delete(self):
        device_info = request.get_json()
        logger.debug(f"Requested to delete device:\n{pformat(device_info)}")

        asdb.delete_device(device_info)


_model_ping_in = api.model('Ping_in', {
    'id': fields.String,
})


@api.route('/device/ping', endpoint='device_ping')
class DevicePing(Resource):
    @api.expect(_model_ping_in)
    def post(self):
        device = request.get_json()
        logger.debug(f'Received ping: {device}')

        uri = current_app.config['RABBITMQ_URI']
        logger.debug(f"Connect to RabbitMQ {uri}")
        with Connection(uri) as conn:
            channel = conn.channel()
            exchange = Exchange('configurations', type='topic', durable=True)

            # Reformatted message
            message = json.dumps({
                'device_id': device['id']
            })
            producer = Producer(exchange=exchange,
                                channel=channel,
                                routing_key=f'cfg.ping')
            producer.publish(message)
        return 200
