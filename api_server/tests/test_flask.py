import ast 
import json
import logging

from flask_login import current_user, login_user
import pytest
import pytest_env

from api_server.database import db 
from db.models import States 

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

    assert right_states == json.loads(rv.data)


def test_register_missing_data(client):
    missing_username = {
        'username': None,
        'password': 'test_password'
    }
    rv_username = client.post('http://localhost:5000/api/v1/register', json=missing_username)
    
    missing_password = {
        'username': None,
        'password': 'test_password'
    }
    rv_password = client.post('http://localhost:5000/api/v1/register', json=missing_password)
    
    assert rv_username.status_code == 400
    assert rv_password.status_code == 400 


def test_register(client):
    existing_user = {
        'username': 'test_user',
        'password': 'test_password'
    }
    rv_existing = client.post('http://localhost:5000/api/v1/register', json=existing_user)

    test_user = {
        'username': 'user',
        'password': 'test_password'
    }
    rv_new = client.post('http://localhost:5000/api/v1/register', json=test_user)

    assert rv_existing.status_code == 400
    assert rv_new.status_code == 200 



def test_login_post_existing_user(client):
    test_json = {
        'username': 'test_user',
        'password': 'test_password'
    }
    rv = client.post('http://localhost:5000/api/v1/login', json=test_json)

    assert rv.status_code == 200 
    assert ast.literal_eval(rv.data.decode('utf-8'))['username'] == test_json['username']


def test_login_post_non_existing_user(client):
    test_json = {
        'username': 'non_existing_user',
        'password': 'non_existing_password'
    }
    rv = client.post('http://localhost:5000/api/v1/login', json=test_json)
    
    assert rv.status_code == 400  