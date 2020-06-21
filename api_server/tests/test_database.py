from datetime import datetime, timedelta
import logging
from pprint import pformat
import uuid

import pytest

import api_server.database as asdb
from db.models import State, Device, Place, User, Token

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)


def test_get_last_states(timescaleDB):
    _ = timescaleDB.query(State). \
        order_by(State.device_id, State.timestamp.desc()). \
            all()
    # to store expected rows 
    right_states = []
    for right_state in _:
        right_states.append(right_state)

    test_query = asdb.get_last_states(
        start_ts=datetime.now() - timedelta(minutes=5),
        place_id=1, 
        db_session=timescaleDB
    )
    db_last_states = []
    for test_state in test_query:
        db_last_states.append(test_state)

    assert right_states == db_last_states 


def test_get_places(timescaleDB):
    places = asdb.get_places(timescaleDB)[0]

    assert places.id == 1, "Place ID is invalid"
    assert places.name == 'KEMZ', "Place name is invalid"
    assert places.num == '8201', "Place number is invalid" 


def test_create_place(timescaleDB):
    test_place_info = {
        'name': 'ELESI', 
        'num': '8203-1',
        'attr_os': ['Windows'],
        'attr_software': ['Matlab'],
        'attr_people': 20,
        'attr_computers': 8,
        'attr_board': False,
        'attr_projector': True
    }

    new_place = asdb.create_place(test_place_info, timescaleDB)

    places_num = timescaleDB.query(Place).count()

    assert new_place.name == test_place_info['name']
    assert new_place.num == test_place_info['num']
    assert new_place.attr_os == test_place_info['attr_os'] 
    assert new_place.attr_software == test_place_info['attr_software']
    assert new_place.attr_people == test_place_info['attr_people']
    assert new_place.attr_computers == test_place_info['attr_computers']
    assert new_place.attr_blackboard == test_place_info['attr_board']
    assert new_place.attr_projector == test_place_info['attr_projector']
    assert places_num == 2 


def test_update_place(timescaleDB):
    test_place_info = {
        'id': 1,
        'name': 'KEMZ', 
        'num': '8201',
        'attr_os': ['Windows'],
        'attr_software': ['Matlab'],
        'attr_people': 20,
        'attr_computers': 8,
        'attr_board': True,
        'attr_projector': True
    }

    asdb.update_place(test_place_info, timescaleDB)
    place = timescaleDB.query(Place).get(test_place_info['id'])

    assert place.name == test_place_info['name'] 
    assert place.num == test_place_info['num']


def test_delete_place(timescaleDB):
    test_place_info = {
        'name': 'Test', 
        'num': '111',
        'attr_os': ['Windows'],
        'attr_software': ['Matlab'],
        'attr_people': 20,
        'attr_computers': 8,
        'attr_board': False,
        'attr_projector': True
    }

    new_place = asdb.create_place(test_place_info, timescaleDB)
    test_place_info['id'] = new_place.id 

    asdb.delete_place(test_place_info, timescaleDB)
    test_place = timescaleDB.query(Place).get(new_place.id)

    assert test_place == None  


def test_update_device(timescaleDB):
    test_device_info = {
        'id': timescaleDB.query(Device.id).first(),
        'name': 'Test Device', 
        'icon_name': 'Test Icon', 
        'type': 'env', 
        'place_id': 1, 
        'config': {}
    }

    asdb.update_device(test_device_info, timescaleDB)

    test_device = timescaleDB.query(Device).get(test_device_info['id'])

    assert test_device.place_id == test_device_info['place_id']
    assert test_device.type == test_device_info['type']
    assert test_device.name == test_device_info['name']


def test_reset_device(timescaleDB):
    device_info = {
        'id': uuid.uuid4(),
        'place_id': 1, 
        'is_installed': True, 
        'name': 'New Test Device',
        'icon_name': 'New Test Icon'
    }
    
    new_device = Device(
                        id=device_info['id'],
                        place_id=device_info['place_id'],
                        register_date=datetime.now(), 
                        is_installed=device_info['is_installed'], 
                        name=device_info['name'],
                        icon_name=device_info['icon_name']
            )
    timescaleDB.add(new_device)
    timescaleDB.commit()

    asdb.reset_device(device_info, timescaleDB)
    reseted_device = timescaleDB.query(Device).get(device_info['id'])
    # TODO delete new device to not trash temp DB 
    assert reseted_device.place_id == None 
    assert reseted_device.is_installed == False  


def test_delete_device(timescaleDB):
    device_info = {
            'id': uuid.uuid4(),
            'place_id': 1, 
            'is_installed': True, 
            'name': 'Device 4 Delete',
        }
        
    new_device = Device(
                        id=device_info['id'],
                        place_id=device_info['place_id'],
                        register_date=datetime.now(), 
                        is_installed=device_info['is_installed'], 
                        name=device_info['name'],
            )

    timescaleDB.add(new_device)
    timescaleDB.commit()

    asdb.delete_device(device_info, timescaleDB)
    check_device = timescaleDB.query(Device).get(device_info['id'])
    
    assert check_device == None  

def test_get_devices(timescaleDB):
    assert len(asdb.get_devices(1, timescaleDB)) == 3 




def test_get_user_data(timescaleDB):
    test_query = asdb.get_user_data("test_user", db_session=timescaleDB)

    assert test_query.username == 'test_user', "No valid username"
    assert test_query.check_password('test_password'), "No valid password"


def test_create_user(timescaleDB):
    new_user = asdb.create_user(
        username='new_test_user', 
        password='new_test_password',
        db_session=timescaleDB
    )

    num_of_users = timescaleDB.query(User).count()

    assert num_of_users == 2, "New user wasn't added to DB"
    assert new_user.username == 'new_test_user', "Username is wrong"
    assert new_user.id == 2, "USER ID is wrong"


def test_save_token(timescaleDB, flask_app):
    test_token = asdb.save_token(
        user_id=1, 
        secret=flask_app.config['SECRET_KEY'],
        db_session=timescaleDB
    )

    check_token = [str(tkn) for tkn in timescaleDB.query(Token.token).first()][0]
    
    assert test_token.token == check_token, "Token is invalid" 


def test_delete_token(timescaleDB, flask_app):
    if timescaleDB.query(Token).count() == 0:
        new_token = asdb.save_token(
            user_id=1, 
            secret=flask_app.config['SECRET_KEY'],
            db_session=timescaleDB
        )

        check_token = new_token.token 
        parent_id = new_token.parent_id
        created_on = new_token.created_on
    else:
        test_token = timescaleDB.query(Token).first()
        
        check_token = test_token.token 
        parent_id = test_token.parent_id  
        created_on = test_token.created_on

    asdb.delete_token(
        user_id=parent_id, 
        created_on=created_on,
        db_session=timescaleDB
    )

    check = timescaleDB.query(Token). \
        filter(Token.token == check_token).first()

    assert check == None, "Token wasn't deleted from DB" 


