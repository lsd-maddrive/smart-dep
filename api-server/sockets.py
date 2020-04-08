import json
import random
import time
from threading import Thread, Event
import math as m

from flask import request, current_app
from flask_socketio import SocketIO, join_room, leave_room
import logging

socketio = SocketIO(cors_allowed_origins="*")

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

_env_state = {
    'device_id': '0',
    'type': 'env',
    'state': {
        'temperature': 25.0,
        'humidity': 40.0,
        'lightness': 35.0
    }
}

class PlaceStateSender(Thread):
    def __init__(self, place_id, period_s):
        self.place_id = place_id
        self.period_s = period_s
        self.enabled = True
        super(PlaceStateSender, self).__init__()

        self.debug = current_app.debug

    def stop(self):
        self.enabled = False
        self.join()

    def run(self):
        while self.enabled:
            time_start = time.time()

            if self.debug:
                light_state = _lights_db[0].copy()
                light_state['state']['enabled'] = bool(random.getrandbits(1))

                env_state = _env_state.copy()
                env_state['ts'] = time.time()
                env_state['state']['temperature'] = m.sin(time.time()/10)*3 + 25
                env_state['state']['humidity'] = m.cos(time.time()/10)*3 + 40

                data = [light_state, env_state]

            logger.debug(f'Send {data} to {self.place_id}')
            socketio.emit('state', data, room=self.place_id)

            passed_time = time.time() - time_start
            sleep_time = self.period_s - passed_time
            if sleep_time < 0:
                logger.warning(
                    f'Time processing requires more time delay, current processing time: {passed_time} [s]')
            else:
                time.sleep(sleep_time)


class PlaceStateSenderManager(object):
    def __init__(self):
        self.threads = {}
        self.threads_started = {}
        self.counters = {}
        self.sid_2_place = {}

    def start_place(self, place_id, sid):
        self.sid_2_place[sid] = place_id
        join_room(place_id)

        if place_id not in self.threads:
            self.threads[place_id] = PlaceStateSender(place_id, 3)
            self.threads_started[place_id] = False
            self.counters[place_id] = 1
        else:
            self.counters[place_id] += 1

        if not self.threads_started[place_id]:
            self.threads[place_id].start()
            self.threads_started[place_id] = True
        elif not self.threads[place_id].is_alive():
            log.warning(f'Thread for {place_id} not alive!')

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
