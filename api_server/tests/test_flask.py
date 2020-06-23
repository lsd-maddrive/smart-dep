import ast 
import copy
from datetime import datetime
import json
import logging
import numpy as np
from pprint import pformat
import sys 
sys.path.append("../")
from time import sleep
import uuid

import pytest
import pytest_env
from werkzeug.datastructures import FileStorage


import database as asdb
# from api_server.database import db 
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
    
    updated_place = timescaleDB.query(Place).get(inp_json['id'])
    check_name = updated_place.name 

    updated_place.name = 'KEMZ'
    # reset changes to temp DB
    timescaleDB.commit()

    assert rv.status_code == 200 
    assert check_name == inp_json['name']


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

from io import BytesIO

def test_place_image_post(client, timescaleDB): 
    data = {}

    with open('./tests/resources/test_img.jpg', 'rb') as fp:
        file_ = FileStorage(fp)
        data['image'] = file_ 

        rv = client.post(
                'http://localhost:5000/api/v1/place/1/image',
                data=data, content_type='multipart/form-data'
            )

    check_image = timescaleDB.query(Place).get(1).image

    # to keep temp DB sustainable 
    place = timescaleDB.query(Place).get(1)
    place.image = None 
    timescaleDB.commit()

    assert rv.status_code == 200  
    assert check_image is not None 


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
        json=inp_json
    )

    data = json.loads(rv.data)
    
    assert rv.status_code == 200 
    assert len(data) == 3 
    assert data[0]['place_id'] == 1 

# !!!!!!!!!!!!!!!!!!!!!!!!!!! FIX IT LENA!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# @pytest.mark.skip(reason="F*ck Up with db, guess I need to meditate")
def test_device_put(client, timescaleDB):
    test_device = timescaleDB.query(Device). \
        order_by(Device.register_date.desc()).first()

    logger.debug(f"TEST DEVICE {test_device.id}")
    logger.debug(f"TEST DEVICE NAME {test_device.name}")

    inp_json = {
        'id': test_device.id,
        'name': 'New device',
        'icon_name': 'New Icon',
        'type': 'env', 
        'place_id': test_device.place_id, 
        'last_ts': 0.0, 
        'config': dict()
    }

    rv = client.put(
        '/api/v1/device',
        json=inp_json
    )

    logger.debug(f"TEST UPDATED DEVICE ID: {timescaleDB.query(Device).get(test_device.id).id}")
    logger.debug(f"TEST UPDATED DEVICE NAME: {timescaleDB.query(Device).get(test_device.id).name}")

    # assert True 


    
    updated_device = timescaleDB.query(Device).get(test_device.id)

    # logger.debug(f"COMPARE IDs\n{updated_device.id}\n{test_device.id}")
    
    # # check_device = copy.deepcopy(updated_device)
    
    # logger.debug(f"UPDATED DEVICE {pformat(updated_device)}")
    # # logger.debug(f"NAME {updated_device.name} | {check_device.name}")
    # logger.debug(f"ICON: {updated_device.icon_name}")
    # # updated_device.icon_name = None 
    # # timescaleDB.commit()

    # logger.debug(f"ALL Devices\n{pformat(timescaleDB.query(Device).all())}")

    

    assert rv.status_code == 200 
    assert updated_device.name == inp_json['name']
    # assert check_device.id == inp_json['id']
    # assert check_device.name == inp_json['name']
    # assert check_device.icon_name == inp_json['icon_name']
    # assert check_device.type == inp_json['type']
    # assert check_device.place_id == inp_json['place_id']
    # assert check_device.config == inp_json['config']



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

