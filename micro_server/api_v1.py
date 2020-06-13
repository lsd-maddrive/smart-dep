from datetime import date, datetime, timedelta
import json
import logging
import os

from flask import request, current_app
from flask_restplus import Resource, Namespace, fields
from pprint import pformat

import database as db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api = Namespace('api/v1', description="Main API namespace")


_model_version = api.model('Version', {
    'version': fields.String,
    'code': fields.String
})


@api.route('/app/version', endpoint='app_last_version')
class Version(Resource):
    @api.marshal_with(_model_version, as_list=True)
    def get(self):
        version = request.args.get('version')
        if version is None:
            version = '0.0'

        with open('sample_code.py') as f:
            code = f.read()

        logger.debug(f'Request to receive app.py with version {version}')

        return {
            'version': version,
            'code': code
        }


_model_register_in = api.model('Register_in', {
    'unique_id': fields.String,
})

_model_register_out = api.model('Register_out', {
    'device_id': fields.String,
})


@api.route('/register', endpoint='register')
class Registration(Resource):
    @api.expect(_model_register_in)
    @api.marshal_with(_model_register_out)
    def post(self):
        logger.debug(request.headers)
        data = request.get_json()

        logger.debug(data)
        unique_id = data['unique_id']

        device_id = 'qmkmemq;ewqvwq,'
        logger.debug(
            f'Device with unique_id ({unique_id}) receives DeviceID ({device_id})')

        return {
            'device_id': device_id
        }
