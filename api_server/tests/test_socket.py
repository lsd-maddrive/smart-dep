import logging
from pprint import pformat
import time

import pytest


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)


def test_socketio_data(sio_client):
    config = {
        'place_id': '8201',
        'period': 1
    }
    time_2_sleep = 3

    expected_obj = {
        'args': [[
            {
                'device_id': '01:01:01:01:01:01',
                'state': {
                    'enabled': False
                },
                'type': 'env'
            },
            {
                'device_id': '11:11:11:11:11:11',
                'state': {
                    'enabled': False
                },
                'type': 'light'
            },
            {
                'device_id': 'FF:FF:FF:FF:FF:FF',
                'state': {
                    'enabled': False
                },
                'type': 'power'
            }
        ]],
        'name': 'state',
        'namespace': '/'
    }

    expected_output = []

    for _ in range(time_2_sleep):
        expected_output.append(expected_obj)

    sio_client.emit('start_states', config)
    time.sleep(time_2_sleep)
    data = sio_client.get_received()
    sio_client.emit('disconnect')

    first_time = data[0]['args'][0][3]['emit_time']
    last_time = data[2]['args'][0][3]['emit_time']

    # remove time from data to be able compare only data
    for d in data:
        d['args'][0].pop(3)

    assert expected_output == data, "data doesn't match"
    assert (last_time - first_time) == (time_2_sleep - 1), "time delta is incorrect"
