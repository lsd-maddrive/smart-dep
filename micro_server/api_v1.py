from datetime import date, datetime, timedelta
import json
import logging
import os
from uuid import UUID

from flask import request, current_app
from flask_restplus import Resource, Namespace, fields, reqparse
from pprint import pformat

import database as db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api = Namespace('api/v1', description="Main API namespace")


_model_appcode_args = reqparse.RequestParser()
_model_appcode_args.add_argument(
    'version',
    type=str,
    help='Version of required app (if not set - return last)',
    required=False)

_model_app_code = api.model('App_code', {
    'version': fields.String,
    'code': fields.String
})


@api.route('/app/version', endpoint='app_code')
class Version(Resource):
    @api.expect(_model_appcode_args)
    @api.marshal_with(_model_app_code)
    def get(self):
        version = request.args.get('version')
        if version is None:
            version = '0.0'

        with open('units/app_code.py') as f:
            code = f.read()

        logger.debug(f'Request to receive app.py with version {version}')

        return {
            'version': version,
            'code': code
        }


_model_unitcode_args = reqparse.RequestParser()
_model_unitcode_args.add_argument(
    'devtype',
    type=str,
    help='Type of device to download code',
    required=True,
    case_sensitive=True)

_model_unit_code = api.model('Unit_code', {
    'code': fields.String,
})


@api.route('/app/unit_code', endpoint='unit_code')
class UnitCode(Resource):
    @api.expect(_model_unitcode_args)
    @api.marshal_with(_model_unit_code)
    def get(self):
        dtype = request.args.get('devtype')

        fpath = os.path.join(f'units/{dtype}.py')
        logger.debug(f'Request to receive {fpath}')

        if not os.path.exists(fpath):
            return f"Unit {dtype} not found", 404

        with open(fpath) as f:
            code = f.read()

        return {
            'code': code
        }


_model_register_in = api.model('Register_in', {
    'unique_id': fields.String,
})

_model_register_out = api.model('Register_out', {
    'device_id': fields.String,
})


@api.route('/app/register', endpoint='register')
class Registration(Resource):
    @api.expect(_model_register_in)
    @api.marshal_with(_model_register_out)
    def post(self):
        data = request.get_json()
        logger.debug(data)
        unique_id = data.get('unique_id')
        if unique_id:
            uid_device = db.get_devices_with_uid(unique_id).one_or_none()
            if uid_device is not None:
                logger.debug(f'Found already existing device: {uid_device}')
                return {
                    'device_id': uid_device.id
                }

        new_device = db.register_device(unique_id)
        logger.debug(f'Registered new device: {new_device}')
        return {
            'device_id': new_device.id
        }


_model_enabled_in = api.model('Enabled_in', {
    'unique_id': fields.String(description='Unique ID of device', required=False),
    'device_id': fields.String,
    'ip_addr': fields.String,
})

_model_enabled_out = api.model('Enabled_out', {
    'type': fields.String,
    'place_id': fields.String,
    'config': fields.Raw,
})


@api.route('/app/enabled', endpoint='enabled')
class DeviceEnabled(Resource):
    @api.expect(_model_enabled_in, validate=True)
    @api.marshal_with(_model_enabled_out)
    @api.response(400, 'Bad request / Invalid data')
    @api.response(403, 'Not Authorized (register required)')
    def post(self):
        data = request.get_json()
        logger.debug(data)

        unique_id = data.get('unique_id')
        device_id = data['device_id']

        try:
            device_uuid = UUID(device_id)
        except:
            return f"Invalid parameter {device_id}", 400

        device = db.set_device_enabled_info(unique_id, device_uuid, data)
        if device is None:
            return "Failed to update device info", 403

        return {
            'type': device.type,
            'place_id': device.place_id,
            'config': device.config
        }
