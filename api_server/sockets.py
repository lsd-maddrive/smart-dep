from datetime import datetime, timedelta
import json
import os
import sys
sys.path.append("..")
import random
import time
from threading import Thread, Event
import math as m
from contextlib import contextmanager

from flask import request, current_app
from flask_socketio import SocketIO, join_room, leave_room
import logging

from db.database import * 

# >>to allow other origins
# >>'*' can be used to instruct the server to allow all origins
socketio = SocketIO(cors_allowed_origins="*")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

time_delta = timedelta(minutes=int(os.getenv('DMINUTES', '5')))


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
    def __init__(self, id_, period_s):
        self.id_ = id_
        self.period_s = period_s
        self.enabled = True
        super(PlaceStateSender, self).__init__()

        # self.debug = current_app.debug
        # self.db_session = db_session

    def stop(self):
        self.enabled = False
        self.join()

    def run(self):
        while self.enabled:
            time_start = time.time()

            logger.debug("INSIDE RUN SOCKETS")
            current_timestamp = datetime.now()
            check_time = current_timestamp - time_delta 
            
            logger.debug("Before DB query")
            # devices = get_devices_states(check_time)
            logger.debug("After DB query")
            # for device in devices:
            #     logger.debug(f"FOR LOOP {device}")
            
            light_state = _lights_db[0].copy()
            light_state['state']['enabled'] = bool(random.getrandbits(1))

            env_state = _env_state.copy()
            env_state['ts'] = time.time()
            env_state['state']['temperature'] = m.sin(
                time.time()/10)*3 + 25
            env_state['state']['humidity'] = m.cos(time.time()/10)*3 + 40

            data = [light_state, env_state]

            logger.debug(f'Send {data} to {self.id_}')
            socketio.emit('state', data, room=self.id_)

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

    def start_place(self, place_id, period, sid):
        id_ = f'{place_id}_{period}'
        self.sid_2_place[sid] = id_
        join_room(id_)

        if id_ not in self.threads:
            self.threads[id_] = PlaceStateSender(id_, period)
            self.threads_started[id_] = False
            self.counters[id_] = 1
        else:
            self.counters[id_] += 1

        if not self.threads_started[id_]:
            self.threads[id_].start()
            self.threads_started[id_] = True
        elif not self.threads[id_].is_alive():
            log.warning(f'Thread for {id_} not alive!')

    def stop_place(self, sid):
        id_ = self.sid_2_place.get(sid)
        if id_ is None:
            return

        if id_ not in self.threads:
            return

        self.counters[id_] -= 1

        if self.counters[id_] <= 0:
            leave_room(id_)
            self.threads[id_].stop()
            del self.threads[id_]


place_manager = PlaceStateSenderManager()


@socketio.on('start_states')
def _socket_handle_start_states(config, db_session=None):
    logger.debug(f"INSIDE SOCKET START STATES")
    session_id = request.sid
    logger.debug(f"SESSION ID {session_id}")
    logger.debug(f'Received config: {config} from {session_id}')
    place_id = config['place_id']
    period_s = config['period']

    place_manager.start_place(place_id, period_s, session_id)


@socketio.on('disconnect')
def _socket_handle_disconnect():
    session_id = request.sid
    place_manager.stop_place(session_id)
    logger.debug(f'Disconnected: {session_id}')
