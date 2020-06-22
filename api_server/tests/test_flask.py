import ast 
import copy
from datetime import datetime
import json
import logging
from pprint import pformat
import sys 
sys.path.append("../")
from time import sleep
import uuid

import pytest
import pytest_env

from db.models import State, Place, Device, User, Token

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)

def test_place_get(client, timescaleDB):
    place = timescaleDB.query(Place). \
        filter(Place.name == 'KEMZ').first()

    place.attr_os = [] 
    place.attr_software = []
    place.attr_computers = 25
    place.attr_people = 10
    place.attr_blackboard = False 
    place.attr_projector = False 
    place.image = None 

    timescaleDB.commit()

    rv = client.get('http://localhost:5000/api/v1/place')
    data = json.loads(rv.data)[0]

    assert rv.status_code == 200 
    assert data['id'] == 1
    assert data['num'] == '8201'
    assert data['name'] == 'KEMZ'
    assert data['attr_os'] == []
    assert data['attr_software'] == []
    assert data['attr_computers'] == 25
    assert data['attr_people'] == 10
    assert data['attr_board'] == False
    assert data['attr_projector'] == False 
    assert data['imageURL'] == None 


def test_place_post(client, timescaleDB):
    inp_json = {
        'num': '8101-3',
        'name': 'Siemens'
    }

    rv = client.post(
        'http://localhost:5000/api/v1/place',
        json=inp_json
    )
    

    num_places = timescaleDB.query(Place).count()
    new_place = timescaleDB.query(Place). \
        filter(Place.name == inp_json['name']).first()

    # to keep temp DB sustainable
    timescaleDB.delete(new_place)

    assert rv.status_code == 200  
    assert num_places == 2 
    assert new_place.name == inp_json['name']
    assert new_place.num == inp_json['num']


def test_place_put(client, timescaleDB):
    inp_json = {
        'id': 1,
        'num': '8201',
        'name': 'New KEMZ'
    }

    rv = client.put(
        'http://localhost:5000/api/v1/place',
        json=inp_json
    )
    
    updated_place = timescaleDB.query(Place).get(1)
    
    reset_place = copy.deepcopy(updated_place)
    reset_place.name = 'KEMZ'
    # reset changes to temp DB
    timescaleDB.commit()

    assert rv.status_code == 200 
    assert updated_place.name == inp_json['name']


def test_place_delete(client, timescaleDB):
    test_place = Place(
        name='toDelete',
        num='0000'
    )

    timescaleDB.add(test_place)
    timescaleDB.commit()

    inp_json = {
        'id': timescaleDB.query(Place.id).filter(Place.name == 'toDelete').first()[0]
    }

    rv = client.delete(
        'http://localhost:5000/api/v1/place',
        json=inp_json
    )

    num_places = timescaleDB.query(Place).count()

    assert rv.status_code == 200  
    assert num_places == 1


def test_device_types_get(client, timescaleDB):
    test_device = timescaleDB.query(Device). \
        order_by(Device.register_date.desc()).first()

    inp_json = {
        'id': test_device.id,
        'name': test_device.name,
        'desc': 'Тест'
    }

    rv = client.get(
        'http://localhost:5000/api/v1/device/types',
        json=inp_json
    )

    assert rv.status_code == 200 


def test_device_states_get(client, timescaleDB):
    test_device = timescaleDB.query(Device). \
        order_by(Device.register_date.desc()).first()

    inp_json = {
        'device_id': test_device.id,
        'type': test_device.type,
        'name': test_device.name,
        'icon_name': test_device.icon_name,
        'ts': None, 
        'state': None
    }

    rv = client.get(
        'http://localhost:5000/api/v1/device/states/1',
        json=inp_json
    )

    data = json.loads(rv.data)

    assert rv.status_code == 200 
    assert len(data) == 3 


def test_device_new_get(client, timescaleDB):
    new_device = Device(
        id=uuid.uuid4(),
        place_id=1,
        register_date=datetime.now(), 
        is_installed=False
    )

    timescaleDB.add(new_device)
    timescaleDB.commit()

    inp_json = {
        'id': None, 
        'ip_addr': None,
        'reg_ts': None
    }

    rv = client.get(
        'http://localhost:5000/api/v1/device/new',
        json=inp_json
    )

    logger.debug(f"{rv.status_code}")
    logger.debug(f"{json.loads(rv.data)}")

    data = json.loads(rv.data)[0]

    check_device = timescaleDB.query(Device). \
                filter(Device.is_installed == False).first()

    check_id = str(check_device.id)

    timescaleDB.delete(check_device)

    assert rv.status_code == 200
    assert data['id'] == check_id
    

def test_device_get(client, timescaleDB):
    test_device = timescaleDB.query(Device). \
        order_by(Device.register_date.desc()).first()

    inp_json = {
        'id': test_device.id,
        'reset': False 
    }

    rv = client.get(
        'http://localhost:5000/api/v1/device',
        json=inp_json, query_string={'place_id': 1}
    )

    data = json.loads(rv.data)
    
    assert rv.status_code == 200 
    assert len(data) == 3 
    assert data[0]['place_id'] == 1 


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


def test_register(client, timescaleDB):
    existing_user = {
        'username': 'test_user',
        'password': 'test_password'
    }
    rv_existing = client.post('http://localhost:5000/api/v1/register', json=existing_user)

    test_user = {
        'username': 'new_user',
        'password': 'new_password'
    }

    rv_new = client.post('http://localhost:5000/api/v1/register', json=test_user)

    test_user_obj = timescaleDB.query(User). \
        filter(User.username == test_user['username']). \
            first()
    
    # to keep temp DB sustainable
    timescaleDB.delete(test_user_obj)

    assert rv_existing.status_code == 400
    assert rv_new.status_code == 200 
    assert ast.literal_eval(rv_new.data.decode('utf-8'))['username'] == test_user['username']
    assert ast.literal_eval(rv_new.data.decode('utf-8'))['role'] == 'guest'


def test_login_post_existing_user(client):
    test_json = {
        'username': 'test_user',
        'password': 'test_password'
    }
    rv = client.post('http://localhost:5000/api/v1/login', json=test_json)

    assert rv.status_code == 200 
    assert ast.literal_eval(rv.data.decode('utf-8'))['username'] == test_json['username']
    assert ast.literal_eval(rv.data.decode('utf-8'))['role'] == 'guest'


def test_login_post_non_existing_user(client):
    test_json = {
        'username': 'non_existing_user',
        'password': 'non_existing_password'
    }
    rv = client.post('http://localhost:5000/api/v1/login', json=test_json)
    
    assert rv.status_code == 400  


def test_logout(client, timescaleDB):

    test_json = {
        'username': 'newer_user', 
        'password': 'newer_password'
    }

    rv = client.post('http://localhost:5000/api/v1/register',
                    json=test_json)

    check_user = timescaleDB.query(User). \
        filter(User.username == test_json['username']).first()

    token_result = timescaleDB.query(Token.token). \
        filter(Token.parent_id == check_user.id).first()
    token = [str(tkn) for tkn in token_result][0]
    
    rv = client.post('http://localhost:5000/api/v1/logout',
                    headers={'Authorization': 'Bearer ' + token}, 
                    json=test_json)
    
    # check_user = timescaleDB.query(User). \
    #     filter(User.username == test_json['username']).first()
    
    timescaleDB.delete(check_user)

    assert rv.status_code == 200  
    assert ast.literal_eval(rv.data.decode('utf-8'))['status'] == 'success'
    assert ast.literal_eval(rv.data.decode('utf-8'))['message'] == 'Successfully logged out.'
    assert ast.literal_eval(rv.data.decode('utf-8'))['username'] == test_json['username']


def test_logout_missing_data(client):
    test_json = {
        'username': 'test_user', 
        'password': 'test_password'
    }

    token = ""
    rv_empty_token = client.post('http://localhost:5000/api/v1/logout',
                    headers={'Authorization': 'Bearer ' + token},
                    json=test_json)

    rv_no_token = client.post('http://localhost:5000/api/v1/logout',
                    headers={'Authorization': 'Bearer '},
                    json=test_json)
    
    assert rv_empty_token.status_code == 400 
    assert rv_no_token.status_code == 400


@pytest.mark.skip(reason="strong dependence on token's life time ")
def test_expiring_token(client, timescaleDB):
    """
        Test is not complite, strong dependence on life time of token
    """
    test_json = {
        'username': 'new_new_user', 
        'password': 'test_password'
    }

    rv = client.post('http://localhost:5000/api/v1/register',
                    json=test_json)
    # HERE 5 SECOND, life time = 7 days! 
    sleep(5)
    user_id = timescaleDB.query(User.id). \
        filter(User.username == test_json['username'])

    token_result = timescaleDB.query(Token.token). \
        filter(Token.parent_id == user_id).first()
    token = [str(tkn) for tkn in token_result][0]

    rv = client.post('http://localhost:5000/api/v1/logout',
                    headers={'Authorization': 'Bearer ' + token}, 
                    json=test_json)
    
    assert rv.status_code == 403 

