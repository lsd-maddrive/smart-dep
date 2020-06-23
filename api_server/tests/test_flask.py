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


@pytest.mark.skip(reason="Data in DB for device won't be updated. db_session issue")
def test_device_put(client, timescaleDB):
    test_device = timescaleDB.query(Device). \
        order_by(Device.register_date.desc()).first()

    inp_json = {
        'id': test_device.id,
        'name': 'New_device',
        'icon_name': 'New_Icon',
        'type': 'env', 
        'place_id': test_device.place_id, 
        'last_ts': 0.0, 
        'config': dict()
    }

    rv = client.put(
        '/api/v1/device',
        json=inp_json
    )

    updated_device = timescaleDB.query(Device).get(test_device.id)

    check_data = {
        'id': updated_device.id,
        'name': updated_device.name, 
        'icon_name': updated_device.icon_name,
        'type': updated_device.type, 
        'place_id': updated_device.place_id, 
        'config': updated_device.unit_config
    }

    # reset data in DB to keep DB sustainable 
    updated_device.name = None
    updated_device.icon_name = None, 
    updated_device.type = 'power'
    updated_device.place_id = 1
    updated_device.unit_config = None 
    timescaleDB.commit()


    assert rv.status_code == 200 
    assert check_data['id'] == inp_json['id']
    assert check_data['name'] == inp_json['name']
    assert check_data['icon_name'] == inp_json['icon_name']
    assert check_data['type'] == inp_json['type']
    assert check_data['place_id'] == inp_json['place_id']
    assert check_data['config'] == inp_json['config']


def test_device_delete(client, timescaleDB):
    new_device = Device(
        place_id=1,
        register_date=datetime.now(), 
        is_installed=False, 
        type='light', 
        name='New_test_device', 
        icon_name="New_test_icon"
    )

    timescaleDB.add(new_device)
    timescaleDB.commit()

    new_test_device = timescaleDB.query(Device). \
                            filter(Device.name == 'New_test_device'). \
                                first()
    
    inp_json = {
        'id': new_test_device.id,
        'reset': False 
    }

    rv = client.delete(
        '/api/v1/device',
        json=inp_json
    )

    all_devices = timescaleDB.query(Device).all()

    assert rv.status_code == 200 
    assert len(all_devices) == 3, "Device wasn't removed from DB"  


@pytest.mark.skip(reason="Data in DB for device won't be updated. db_session issue")
def test_device_delete_reset(client, timescaleDB):
    new_device = Device(
        place_id=1,
        register_date=datetime.now(), 
        is_installed=False, 
        type='light', 
        name='Reset_device', 
        icon_name="Reset_icon"
    )

    timescaleDB.add(new_device)
    timescaleDB.commit()

    new_test_device = timescaleDB.query(Device). \
                            filter(Device.name == 'Reset_device'). \
                                first()
    
    inp_json = {
        'id': new_test_device.id,
        'reset': True 
    }

    rv = client.delete(
        '/api/v1/device',
        json=inp_json
    )

    reseted_device = timescaleDB.query(Device).get(new_test_device.id)

    check_data = {
        'is_installed': reseted_device.is_installed,
        'type': reseted_device.type,
        'place_id': reseted_device.place_id, 
        'config': reseted_device.unit_config 
    }

    # logger.debug(f"RESET DEVICE\n{reseted_device}")

    # remove test device from DB to keep DB sustainable 
    timescaleDB.delete(reseted_device)
    timescaleDB.commit()

    logger.debug(f"All DEVICES:\n{timescaleDB.query(Device).all()}")


    assert rv.status_code == 200 
    assert check_data['is_installed'] == False 
    assert check_data['type'] == None 
    assert check_data['place_id'] == None 
    assert check_data['config'] == None 


def test_device_ping(client, timescaleDB):
    test_device = timescaleDB.query(Device). \
        order_by(Device.register_date.desc()).first()
    
    inp_json = {
        'id': str(test_device.id) 
    }

    rv = client.post(
        '/api/v1/device/ping', 
        json=inp_json
    )

    assert rv.status_code == 200  


def test_device_cmd(client, timescaleDB):
    test_device = timescaleDB.query(Device). \
        order_by(Device.register_date.desc()).first()

    inp_json = {
        'device_id': str(test_device.id),
        'place_id': test_device.place_id, 
        'type': test_device.type,
        'cmd': { 'enable': True }
    }

    rv = client.post(
        '/api/v1/device/cmd', 
        json=inp_json
    )

    assert rv.status_code == 200  


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

