from datetime import datetime, timedelta
import json
import logging
import os
import sys
sys.path.append("..")

# import random
import time
from threading import Thread, Event
import math as m
from contextlib import contextmanager

from flask import request, current_app
from flask_socketio import SocketIO, join_room, leave_room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import api_server.database as asdb


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
    def __init__(self, id_, period_s, db_url):
        self.id_ = id_
        self.period_s = period_s
        self.enabled = True
        self.db_url = db_url 
        super(PlaceStateSender, self).__init__()

    def stop(self):
        self.enabled = False
        self.join()

    def run(self):
        engine = create_engine(self.db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        while self.enabled:
            time_start = time.time()

            current_timestamp = datetime.now()
            check_time = current_timestamp - time_delta 
            
            devices = asdb.get_devices_states(check_time, session)
            data = [] 
            for device in devices: 
                data.append(
                    {
                        'device_id': device.device_id, 
                        'type': device.type, 
                        'state': device.state, 
                    }
                )
            
            logger.debug(f'Send {data} to {self.id_}')
            socketio.emit('state', data, room=self.id_)

            passed_time = time.time() - time_start
            sleep_time = self.period_s - passed_time
            
            if sleep_time < 0:
                logger.warning(
                    f'Time processing requires more time delay, current processing time: {passed_time} [s]')
            else:
                time.sleep(sleep_time)
        
        session.close()


class PlaceStateSenderManager(object):
    def __init__(self):
        self.threads = {}
        self.threads_started = {}
        self.counters = {}
        self.sid_2_place = {}

    def start_place(self, place_id, period, sid, db_url):
        id_ = f'{place_id}_{period}'
        self.sid_2_place[sid] = id_
        join_room(id_)

        if id_ not in self.threads:
            self.threads[id_] = PlaceStateSender(id_, period, db_url)
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
def _socket_handle_start_states(config):
    session_id = request.sid
    logger.debug(f"SESSION ID {session_id}")
    logger.debug(f'Received config: {config} from {session_id}')
    place_id = config['place_id']
    period_s = config['period']
    current_db_url = current_app.config["SQLALCHEMY_DATABASE_URI"] 

    place_manager.start_place(place_id, period_s, session_id, current_db_url)


@socketio.on('disconnect')
def _socket_handle_disconnect():
    session_id = request.sid
    place_manager.stop_place(session_id)
    logger.debug(f'Disconnected: {session_id}')
