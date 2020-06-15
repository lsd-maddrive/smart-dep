import datetime
import json
import logging
import os
import time

from flask import request, current_app
from flask_restplus import Resource, Namespace, fields, reqparse
from kombu import Connection, Exchange, Producer
from pprint import pformat

import database as asdb

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api = Namespace('api/v1', description="Main API namespace")


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
    # @api.marshal_with(_model_place_get, as_list=True)
    def get(self):
        places = asdb.get_places()
        result_places = []
        for place in places:
            result_places.append({
                'id': place.id,
                'num': place.num,
                'name': place.name,
                'attr_os': place.attr_os,
                'attr_software': place.attr_software,
                'attr_computers': place.attr_computers,
                'attr_people': place.attr_people,
                'attr_board': place.attr_blackboard,
                'attr_projector': place.attr_projector,
            })

        logger.debug(f"Request places: {result_places}")

        return result_places

    @api.expect(_model_place_new, validate=True)
    def post(self):
        place_info = request.get_json()
        logger.debug(f"Request to create place:\n{pformat(place_info)}")

        new_place = asdb.create_place(place_info)
        logger.debug(f'Created new place: {new_place}')

    @api.expect(_model_place_new, validate=True)
    def put(self):
        place_info = request.get_json()
        logger.debug(f"Request to update place:\n{pformat(place_info)}")

        asdb.update_place(place_info)

    @api.expect(_model_place_del, validate=True)
    def delete(self):
        place_info = request.get_json()
        logger.debug(f"Request to delete place:\n{pformat(place_info)}")

        asdb.delete_place(place_info)


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


_model_state = api.model('State', {
    'device_id': fields.String,
    'type': fields.String,
    'name': fields.String,
    'ts': fields.Float,
    'state': fields.Raw,
})


@api.route('/device/states/<string:place_id>', endpoint='devices_states')
@api.param('place_id', 'ID of place')
class UnitsStates(Resource):
    @api.marshal_with(_model_state, as_list=True)
    def get(self, place_id):
        try:
            back_duration_s = int(request.args.get('duration_s', 5*60))
        except:
            back_duration_s = 5*60

        logger.debug(f'Requested device states for place: {place_id}')
        start_ts = datetime.datetime.now() - datetime.timedelta(seconds=back_duration_s)

        states = asdb.get_last_states(
            start_ts, place_id
        )
        logger.debug(f"Received states: {states}")

        result_states = []
        for st in states:
            result_states.append(
                {
                    'device_id': st.get_did(),
                    'name': st.device.name,
                    'type': st.device.type,
                    'state': st.state,
                    'ts': st.timestamp.timestamp(),
                }
            )

        logger.debug(f"Request devices states: {result_states}")

        return result_states


_model_device_new = api.model('Device_new', {
    'id': fields.String,
    'ip_addr': fields.String,
    'reg_ts': fields.Raw,
})


@api.route('/device/new', endpoint='new_devices')
class DevicesNew(Resource):
    @api.marshal_with(_model_device_new, as_list=True)
    def get(self):
        devices = asdb.get_new_devices()

        result = []
        for dev in devices:
            result.append({
                'id': dev.get_id(),
                'ip_addr': dev.ip_addr,
                'reg_ts': dev.register_date.timestamp()
            })

        logger.debug(f"Request new devices:\n{pformat(result)}")

        return result


_model_device_get_args = reqparse.RequestParser()
_model_device_get_args.add_argument(
    'place_id',
    type=int,
    help='Place ID',
    required=True)


_model_device = api.model('Device', {
    'id': fields.String,
    'name': fields.String,
    'type': fields.String,
    'place_id': fields.Integer,
    'config': fields.Raw,
})

_model_device_del = api.model('Device_del', {
    'id': fields.String,
    'reset': fields.Boolean
})


@api.route('/device', endpoint='device_RUD')
class Device(Resource):
    @api.expect(_model_device_get_args)
    @api.marshal_with(_model_device, as_list=True)
    def get(self):
        place_id = request.args.get('place_id')
        logger.debug(f"Request devices for place: {place_id}")

        devices = asdb.get_devices(place_id)

        result_devices = []
        for dev in devices:
            result_devices.append({
                'id': str(dev.id),
                'name': dev.name,
                'type': dev.type,
                'place_id': dev.place_id,
                'config': dev.unit_config,
            })

        logger.debug(f"Request devices: {result_devices}")
        return result_devices

    @api.expect(_model_device, validate=True)
    def put(self):
        device_info = request.get_json()
        logger.debug(f"Request to update device:\n{pformat(device_info)}")

        asdb.update_device(device_info)
        rabbit_reset_device(device_info['id'])

    @api.expect(_model_device_del, validate=True)
    def delete(self):
        device_info = request.get_json()
        logger.debug(f"Request to delete device:\n{pformat(device_info)}")

        if device_info['reset']:
            asdb.reset_device(device_info)
        else:
            asdb.delete_device(device_info)
        rabbit_reset_device(device_info['id'])


_model_ping = api.model('Device_ping', {
    'id': fields.String,
})


@api.route('/device/ping', endpoint='device_ping')
class DevicePing(Resource):
    @api.expect(_model_ping, validate=True)
    def post(self):
        device = request.get_json()
        logger.debug(f'Request to ping: {device}')

        rabbit_ping_device(device['id'])


_model_command = api.model('Device_command', {
    'device_id': fields.String,
    'place_id': fields.Integer,
    'type': fields.String,
    'cmd': fields.Raw,
})


@api.route('/device/cmd', endpoint='device_cmd')
class DeviceCommand(Resource):
    @api.expect(_model_command, validate=True)
    def post(self):
        data = request.get_json()
        logger.debug(f'Request to send command: {data}')

        place_id = data['place_id']
        type_ = data['type']
        device_id = data['device_id']
        cmd = data['cmd']
        source_id = 'api'

        rabbit_send_command(
            device_id,
            place_id,
            type_,
            cmd,
            source_id
        )

# RabbitMQ functions


def rabbit_ping_device(device_id):
    uri = current_app.config['RABBITMQ_URI']
    logger.debug(f"Connect to RabbitMQ {uri}")
    with Connection(uri) as conn:
        exchange = Exchange('configurations', type='topic', durable=True)
        producer = Producer(exchange=exchange,
                            channel=conn.channel(),
                            routing_key=f'cfg.ping')

        message = json.dumps({
            'device_id': device_id,
            'ts': time.time()
        })
        producer.publish(message)


def rabbit_reset_device(device_id):
    uri = current_app.config['RABBITMQ_URI']
    logger.debug(f"Connect to RabbitMQ {uri}")
    with Connection(uri) as conn:
        exchange = Exchange('configurations', type='topic', durable=True)
        producer = Producer(exchange=exchange,
                            channel=conn.channel(),
                            routing_key=f'cfg.reset')

        message = json.dumps({
            'device_id': device_id,
            'ts': time.time()
        })
        producer.publish(message)


def rabbit_send_command(device_id, place_id, type_, cmd, source_id):
    uri = current_app.config['RABBITMQ_URI']
    logger.debug(f"Connect to RabbitMQ {uri}")

    with Connection(uri) as conn:
        channel = conn.channel()
        exchange = Exchange('commands', type='topic', durable=True)
        producer = Producer(exchange=exchange,
                            channel=channel,
                            routing_key=f'cmd.{place_id}.{type_}')

        message = json.dumps({
            'device_id': device_id,
            'data': cmd,
            'source_id': source_id,
            'ts': time.time()
        })

        producer.publish(message)
    return f'Message sent: {message}'
