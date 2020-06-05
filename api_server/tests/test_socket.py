import logging
import time 

import pytest

from db.database import db 
from db.models import * 


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)


def test_socketio(sio_client):
    config = {
        'place_id': '8201',
        'period': 1
    }

    sio_client.emit('start_states', config)
    time.sleep(3)

    # work, consists of correct data x 3 
    data = sio_client.get_received()
    logger.debug(f'DATA IN TEST: {data}')

    sio_client.emit('disconnect')

    time.sleep(3)

    assert True

