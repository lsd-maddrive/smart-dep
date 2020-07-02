import logging
from pprint import pformat
import time

import pytest
from sqlalchemy import asc

from db.models import Place, Device 


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)


def test_socketio_start_states(sio_client, timescaleDB):
    config = {
        'placeId': 1,
        'period': 1
    }
    time_2_sleep = 3

    sio_client.emit('start_states', config)
    time.sleep(time_2_sleep)
    data = sio_client.get_received()
    sio_client.emit('disconnect')

    first_time = data[0]['args'][0][0]['emit_time']
    last_time = data[2]['args'][0][2]['emit_time']
    check_length = len(data[0]['args'][0])
    check_data = data[0]['args'][0]

    check_places = timescaleDB.query(Place).first()
    devices = timescaleDB.query(Device). \
        order_by(Device.register_date.asc()).all()
    
    devices_id = [str(devices[i].id) for i in range(len(devices))]

    assert round(last_time - first_time) == (time_2_sleep - 1), "time delta is incorrect"
    assert len(data) == 3, "Number of sended banch is wrong (1 banch * period)"
    assert check_length == 3, "Number of Place Data is wrong"
    assert check_data[0]['device_id'] in devices_id, f"Device ID {check_data[0]['device_id']} is wrong"
    assert check_data[1]['device_id'] in devices_id, f"Device ID {check_data[1]['device_id']} is wrong"
    assert check_data[2]['device_id'] in devices_id, f"Device ID {check_data[2]['device_id']} is wrong"