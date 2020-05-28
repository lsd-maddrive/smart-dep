import copy 
import json
import logging

import pytest

from db.database import db 
from db.models import * 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)

def test_powers_request(timescaleDB, client):
    _ = timescaleDB.query(States.device_id, States.state, States.type). \
                    filter(States.type == 'power'). \
                    order_by(States.device_id)
    # to store expected rows 
    right_states = []
    for right_state in _:
        right_states.append(
            {
            'state': right_state.state,
            'device_id': right_state.device_id,
            'type': right_state.type
            }
        )
    
    rv = client.get('http://localhost:5000/api/v1/place/8201/powers')
    # TODO: add message with details if test failed 
    assert right_states == json.loads(rv.data)

def test_lights_request(timescaleDB, client):
    _ = timescaleDB.query(States.device_id, States.state, States.type). \
                    filter(States.type == 'light'). \
                    order_by(States.device_id)
    # to store expected rows 
    right_states = []
    for right_state in _:
        right_states.append(
            {
            'state': right_state.state,
            'device_id': right_state.device_id,
            'type': right_state.type
            }
        )
    
    rv = client.get('http://localhost:5000/api/v1/place/8201/lights')
    # TODO: add message with details if test failed 
    assert right_states == json.loads(rv.data)

def test_place_request(timescaleDB, client):
    right_states = []
    right_states.append(
        {
            'id': '8201',
            'name': '8201',
        }
    )
    rv = client.get('http://localhost:5000/api/v1/place')
    # TODO: add message with details if test failed 
    assert right_states == json.loads(rv.data)

def test_socketio_client_is_connected(sio_client):
    assert sio_client.is_connected()

# TODO: how to check in assert? 
def test_socketio_disconnect(sio_client):
    sio_client.emit('disconnect')
    assert True 


def test_socketio(sio_client, timescaleDB):
    config = {
        'place_id': '8201',
        'period': 5
    }
    tmo = copy.copy(timescaleDB)
    sio_client.emit('start_states', config)
    # logger.debug(f"TEST: {sio_client.get_received()}")
    # logger.debug(f"EMIT {sio_client.emit('start_states', config)}")
    
    assert True