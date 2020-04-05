import json
import random
import time
from threading import Thread, Event

from flask import Flask, request
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room
import logging

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


_lights_db = [
    {
        'device_id': '0',
        'type': 'light',
        'state': {
            'enabled': True
        }
    }
]


class PlaceStateSender(Thread):
    def __init__(self, place_id, period_s):
        self.place_id = place_id
        self.period_s = period_s
        self.enabled = True
        super(PlaceStateSender, self).__init__()

    def stop(self):
        self.enabled = False
        self.join()

    def run(self):
        while self.enabled:
            time_start = time.time()

            state = _lights_db[0].copy()
            state['state']['enabled'] = bool(random.getrandbits(1))

            logger.debug(f'Send {state} to {self.place_id}')
            socketio.emit('state', state, room=self.place_id)

            passed_time = time.time() - time_start
            sleep_time = self.period_s - passed_time
            if sleep_time < 0:
                logger.warning(f'Time processing requires more time delay, current processing time: {passed_time} [s]')
            else:
                time.sleep(sleep_time)


class PlaceStateSenderManager(object):
    def __init__(self):
        self.threads = {}
        self.counters = {}
        self.sid_2_place = {}

    def start_place(self, place_id, sid):
        self.sid_2_place[sid] = place_id
        join_room(place_id)

        if place_id not in self.threads:
            self.threads[place_id] = PlaceStateSender(place_id, 10)
            self.counters[place_id] = 1
        else:
            self.counters[place_id] += 1

        if not self.threads[place_id].is_alive():
            self.threads[place_id].start()

    def stop_place(self, sid):
        place_id = self.sid_2_place.get(sid)
        if place_id is None:
            return

        if place_id not in self.threads:
            return

        self.counters[place_id] -= 1

        if self.counters[place_id] <= 0:
            leave_room(place_id)
            self.threads[place_id].stop()
            del self.threads[place_id]
            del self.counters[place_id]


place_manager = PlaceStateSenderManager()


@socketio.on('start_states')
def _socket_handle_start_states(config):
    session_id = request.sid
    logger.debug(f'Received config: {config} from {session_id}')
    place_id = config['place_id']

    place_manager.start_place(place_id, session_id)


@socketio.on('set_state')
def _socket_handle_start_states(state):
    session_id = request.sid
    logger.debug(f'Received state: {state} from {session_id}')


@socketio.on('disconnect')
def _socket_handle_disconnect():
    session_id = request.sid
    place_manager.stop_place(session_id)
    logger.debug(f'Disconnected: {session_id}')


_model_light_state = api.model('LightState', {
    'enabled': fields.Boolean
})

_model_lights = api.model('Light', {
    'device_id': fields.String,
    'type': fields.String,
    'state': fields.Nested(_model_light_state),
})


@api.route('/lights', endpoint='lights')
class Rooms(Resource):
    @api.marshal_with(_model_lights, as_list=True)
    def get(self):
        data = _lights_db
        logger.debug(f'Send lights: {data}')
        return data


_rooms_db = [
    {
        'id': '8201',
        'name': "KEMZ",
    }
]


_model_rooms = api.model('Room', {
    'id': fields.String,
    'name': fields.String,
})

@api.route('/rooms', endpoint='rooms')
class Rooms(Resource):
    @api.marshal_with(_model_rooms, as_list=True)
    def get(self):
        return _rooms_db


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=True)
    # app.run(debug=True)
