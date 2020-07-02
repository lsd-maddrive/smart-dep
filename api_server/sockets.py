from datetime import datetime, timedelta
import logging
import os
from pprint import pformat

import time
from threading import Thread
from contextlib import contextmanager

from flask import request, current_app
from flask_socketio import SocketIO, join_room, leave_room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database as asdb


socketio = SocketIO(cors_allowed_origins="*")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

time_delta = timedelta(minutes=int(os.getenv('DMINUTES', '5')))


class PlaceStateSender(Thread):
    def __init__(self, id_, period_s, place_id, db_url):
        self.id_ = id_
        self.place_id = place_id
        self.period_s = period_s
        self.enabled = True
        self.db_url = db_url
        super(PlaceStateSender, self).__init__()

    def stop(self):
        self.enabled = False
        self.join()

    def run(self):

        logger.debug(f"DB URL: {self.db_url}")
        engine = create_engine(self.db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        while self.enabled:
            time_start = time.time()
            start_ts = datetime.now() - time_delta

            states = asdb.get_last_states(start_ts, self.place_id, session)
            data = []
            for st in states:
                data.append(
                    {
                        'device_id': st.get_did(),
                        'type': st.device.type,
                        'state': st.state,
                        'ts': st.timestamp.timestamp(),
                        # time of emitting 'state' event - fot pytest
                        'emit_time': datetime.now().timestamp()
                    }
                )
            logger.debug(f'Send:\n{pformat(data)}\nto {self.id_}')
            
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
            self.threads[id_] = PlaceStateSender(id_, period, place_id, db_url)
            self.threads_started[id_] = False
            self.counters[id_] = 1
        else:
            self.counters[id_] += 1

        if not self.threads_started[id_]:
            self.threads[id_].start()
            self.threads_started[id_] = True
        elif not self.threads[id_].is_alive():
            logger.warning(f'Thread for {id_} not alive!')

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
    place_id = config['placeId']
    period_s = config['period']
    current_db_url = current_app.config["SQLALCHEMY_DATABASE_URI"]

    place_manager.start_place(place_id, period_s, session_id, current_db_url)


# Are stop_states and disconnect the same thing???
@socketio.on('stop_states')
def _socket_handle_stop_states():
    session_id = request.sid
    logger.debug(f"SESSION ID {session_id}")
    
    place_manager.stop_place(session_id)


@socketio.on('disconnect')
def _socket_handle_disconnect():
    session_id = request.sid
    place_manager.stop_place(session_id)
    logger.debug(f'Disconnected: {session_id}')
