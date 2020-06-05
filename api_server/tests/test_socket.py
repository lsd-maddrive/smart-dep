import logging

import pytest

from db.database import db 
from db.models import * 


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)


def test_socketio_client_is_connected(sio_client):
    assert sio_client.is_connected()


def test_socketio(sio_client):
    config = {
        'place_id': '8201',
        'period': 1
    }

    sio_client.emit('start_states', config)
    
    assert True


# TODO: how to check in assert? 
def test_socketio_disconnect(sio_client):
    sio_client.emit('disconnect')
    assert True 