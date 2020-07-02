import datetime
from io import BytesIO
import json
import logging
import os

from flask import request, current_app, jsonify, send_file
from flask_restplus import Resource, Namespace, fields, reqparse, abort
from pprint import pformat
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage
from werkzeug.security import check_password_hash

import auth
import database as asdb
import messages as msgs

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

_model_place_update = api.model('Place_new', {
    'id': fields.Integer,
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
                'imageURL': None if place.image == None else f"place/{place.id}/image"
            })

        logger.debug(f"Request places: {result_places}")

        return result_places

    @api.expect(_model_place_new, validate=True)
    def post(self):
        place_info = request.get_json()
        logger.debug(f"Request to create place:\n{pformat(place_info)}")

        new_place = asdb.create_place(place_info)
        logger.debug(f'Created new place: {new_place}')

    @api.expect(_model_place_update, validate=True)
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


file_upload = reqparse.RequestParser()
file_upload.add_argument('image',
                        type=FileStorage,
                        location='files',
                        help='Place Image',
                        required=True
                        )

@api.route('/place/<string:id>/image', endpoint='place_image', methods=['GET', 'POST'])
@api.param('id', 'ID of place')
class PlaceImage(Resource):
    @api.expect(file_upload)
    def post(self, id):
        logger.debug(f"API Place ID: {id}")
        args = file_upload.parse_args()
        # args = request.files['image']

        logger.debug(f"ARGS: {args}")

        uploaded_img = args['image'].read()

        # check if place with id - is existed
        if asdb.get_place_data(id) is None:
            logger.critical(f"Place with ID: {id} doesn't exist")
            abort(404)

        # save to DB
        asdb.save_place_image(id, uploaded_img)


    def get(self, id):
        place = asdb.get_place_data(id)

        return send_file(BytesIO(place.image), mimetype='image/png')


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
    'icon_name': fields.String,
    'ts': fields.Float,
    'state': fields.Raw,
})


@api.route('/device/states/<string:place_id>', endpoint='devices_states')
@api.param('place_id', 'ID of place')
class DevicesStates(Resource):
    @api.marshal_with(_model_state, as_list=True)
    def get(self, place_id):
        logger.debug(f'Requested device states for place: {place_id}')
        devices = asdb.get_devices(place_id)
        result_states = []
        for dev in devices:
            last_st = dev.last_state.first()

            result_states.append(
                {
                    'device_id': dev.get_id(),
                    'name': dev.name,
                    'icon_name': dev.icon_name,
                    'type': dev.type,
                    'state': last_st.state if last_st else {},
                    'ts': last_st.timestamp.timestamp() if last_st else dev.update_date.timestamp(),
                }
            )

        logger.debug(f"Request devices states:\n{pformat(result_states)}")

        return result_states


_model_device_new = api.model('Device_new', {
    'id': fields.String,
    'ip_addr': fields.String,
    'reg_ts': fields.Float,
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
    'icon_name': fields.String,
    'type': fields.String,
    'place_id': fields.Integer,
    'last_ts': fields.Float,
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
            last_st = dev.last_state.first()

            result_devices.append({
                'id': str(dev.id),
                'name': dev.name,
                'icon_name': dev.icon_name,
                'type': dev.type,
                'place_id': dev.place_id,
                'config': dev.unit_config,
                'last_ts': last_st.timestamp.timestamp() if last_st else dev.enabled_date.timestamp(),
            })

        logger.debug(f"Request devices: {result_devices}")
        return result_devices

# PYtest - skipped, because behavior is undefined 
    @api.expect(_model_device, validate=True)
    def put(self):
        device_info = request.get_json()
        logger.debug(f"Request to update device:\n{pformat(device_info)}")

        asdb.update_device(device_info)

        if not current_app.config['TESTING']:
            msgs.reset_device(
                current_app.config['RABBITMQ_URI'],
                device_info['id'])

# if reset == True -> PYtest - skipped, because behavior is undefined 
    @api.expect(_model_device_del, validate=True)
    def delete(self):
        device_info = request.get_json()
        logger.debug(f"Request to delete device:\n{pformat(device_info)}")

        if device_info['reset']:
            asdb.reset_device(device_info)
        else:
            asdb.delete_device(device_info)
        
        if not current_app.config['TESTING']:
            msgs.reset_device(
                current_app.config['RABBITMQ_URI'],
                device_info['id'])


_model_ping = api.model('Device_ping', {
    'id': fields.String,
})


@api.route('/device/ping', endpoint='device_ping')
class DevicePing(Resource):
    @api.expect(_model_ping, validate=True)
    def post(self):
        device = request.get_json()
        logger.debug(f'Request to ping: {device}')

        if not current_app.config['TESTING']:
            msgs.ping_device(
                current_app.config['RABBITMQ_URI'],
                device['id'])


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

        if not current_app.config['TESTING']:
            msgs.send_command(
                current_app.config['RABBITMQ_URI'],
                device_id,
                place_id,
                type_,
                cmd,
                source_id
            )

_model_user_credentials = api.model('User_credentials', {
    'username': fields.String,
    'password': fields.String,
})


@api.route('/register', methods=['POST'])
class Signup(Resource):
    @api.expect(_model_user_credentials, validate=True)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            logger.critical(f"Username or password is missing")
            # Raise a HTTPException for the given http_status_code
            abort(400)

        try:
            new_user = asdb.create_user(username, password)
        except IntegrityError as err:
            logger.critical(f"User '{username}' already exists")
            abort(400)

        new_token = asdb.save_token(
            new_user.id,
            current_app.config['SECRET_KEY']
        )

        responseObject = {
            'token': new_token.token,
            'username': new_user.username,
            'role': new_user.role
        }

        return jsonify(responseObject)


@api.route('/login', methods=['POST'])
class Login(Resource):
    @api.expect(_model_user_credentials, validate=True)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            logger.critical(f"Username or password is missing")
            # Raise a HTTPException for the given http_status_code
            abort(400)

        user = asdb.get_user_data(username)
        if user is None:
            logger.critical(
                f"Login failed! User \"{username}\" doesn't exist")
            # Raise a HTTPException for the given http_status_code
            abort(400)

        if not check_password_hash(user.password_hash, password):
            logger.critical(
                f"Login failed! User \"{username}\" password is invalid"
            )
            # Raise a HTTPException for the given http_status_code
            abort(400)

        new_token = asdb.save_token(user.id, current_app.config['SECRET_KEY'])

        responseObject = {
            'token': new_token.token,
            'username': user.username,
            'role': user.role
        }

        return jsonify(responseObject)


def verify_request_header():
    """
        Check if request.header consists of field 'Authorization'
        and token

        Returns:
            token (string)
    """
    if not current_app.config['SECRET_KEY']:
        return

    auth_header = request.headers.get('Authorization')
    if auth_header.lower().startswith('bearer'):
        try:
            auth_token = auth_header.split(" ")[1]
            if len(auth_token) == 0:
                raise IndexError
            return auth_token
        except IndexError as err:
            logger.critical(f"TOKEN NOT FOUND IN REQUEST HEADER")
            abort(400)
    else:
        logger.critical(f"HEADER 'Authorization' NOT FOUND")
        abort(400)


# TODO: think about automatic removing expired tokens from DB
@api.route('/logout', methods=['POST'])
class Logout(Resource):
    @api.expect(_model_user_credentials, validate=True)
    def post(self):
        """
            This method is for checking functionality of token and headers
            Maybe in the future it will be removed
        """
        auth_token = verify_request_header()

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user_id, token_iat = auth.decode_token(
            auth_token,
            current_app.config['SECRET_KEY']
        )

        if isinstance(user_id, int):
            asdb.delete_token(user_id, token_iat)
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged out.',
                'username': username,
            }

            return jsonify(responseObject)
        else:
            logger.critical(f"{user_id}")
            abort(403)
