import copy 
from datetime import datetime, timedelta
import logging
from pprint import pformat
import sys 
sys.path.append("../")
import uuid

import pytest
from werkzeug.security import check_password_hash

import database as asdb
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

    assert right_states == db_last_states, "Last states are wrong" 


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

    # remove new place to keep temp DB sustainable 
    timescaleDB.delete(new_place)

    assert new_place.name == test_place_info['name'], "Name of new place is wrong"
    assert new_place.num == test_place_info['num'], "Number of new place is wrong"
    assert new_place.attr_os == test_place_info['attr_os'], "OS for new place is wrong" 
    assert new_place.attr_software == test_place_info['attr_software'], "Software for new place is wrong"
    assert new_place.attr_people == test_place_info['attr_people'], "Number of people for new place is wrong"
    assert new_place.attr_computers == test_place_info['attr_computers'], "Number of computers for new place is wrong"
    assert new_place.attr_blackboard == test_place_info['attr_board'], "Status of blackboard existance is wrong"
    assert new_place.attr_projector == test_place_info['attr_projector'], "Status of projector existance is wrong"
    assert places_num == 2, "Number of places is wrong"


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
    test_place = timescaleDB.query(Place).get(test_place_info['id'])
    
    check_data = {
        'attr_os': test_place.attr_os,
        'attr_software': test_place.attr_software,
        'attr_people': test_place.attr_people,
        'attr_computers': test_place.attr_computers,
        'attr_board': test_place.attr_blackboard,
        'attr_projector': test_place.attr_projector
    }

    # reset updated data to keep temp DB sustainable 
    test_place.attr_os = [] 
    test_place.attr_software = []
    test_place.attr_people = 10 
    test_place.attr_computers = 25 
    test_place.attr_blackboard = False 
    test_place.attr_projector = False 
    timescaleDB.commit() 
    
    assert check_data['attr_os'] == test_place_info['attr_os'], "OS array is wrong"
    assert check_data['attr_software'] == test_place_info['attr_software'], "Software array is wrong"
    assert check_data['attr_people'] == test_place_info['attr_people'], "People number is wrong"
    assert check_data['attr_computers'] == test_place_info['attr_computers'], "Computer number is wrong"
    assert check_data['attr_board'] == test_place_info['attr_board'], "Blackboard status is wrong"
    assert check_data['attr_projector'] == test_place_info['attr_projector'], "Projector status is wrong"


def test_delete_place(timescaleDB):
    new_place = Place(
        name='Test', 
        num='111', 
        attr_os=['Windows'],
        attr_software=['Matlab'],
        attr_people=20,
        attr_computers=8,
        attr_blackboard=False,
        attr_projector=True
    )
    timescaleDB.add(new_place)
    timescaleDB.commit()

    test_place_info = {
        'id': timescaleDB.query(Place.id).filter(Place.name == 'Test').first(),
        'name': new_place.name, 
        'num': new_place.num,
        'attr_os': new_place.attr_os,
        'attr_software': new_place.attr_software,
        'attr_people': new_place.attr_people,
        'attr_computers': new_place.attr_computers,
        'attr_board': new_place.attr_blackboard,
        'attr_projector': new_place.attr_projector
    }

    asdb.delete_place(test_place_info, timescaleDB)
    test_place = timescaleDB.query(Place).get(new_place.id)

    assert test_place == None, "Place wasn't removed" 


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
    logger.debug(
        f"ALL DEVICES:\n" \
        f"{pformat(timescaleDB.query(Device).all())}"
    )

    device = timescaleDB.query(Device).get(test_device_info['id'])
    test_device = copy.deepcopy(device)

    # reset updated data to keep temp DB sustainable 
    device.name = None 
    device.icon_name = None 
    timescaleDB.commit()

    assert test_device.place_id == test_device_info['place_id'], "Place ID for device wasn't updated"
    assert test_device.type == test_device_info['type'], "Type of device wasn't updated"
    assert test_device.name == test_device_info['name'], "Name of device wasn't updated"


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
    
    # remove new device for test to keep temp DB sustainable 
    timescaleDB.delete(new_device)

    assert reseted_device.place_id == None, "Place ID for devices wasn't reseted" 
    assert reseted_device.is_installed == False, "Device is installed, expected NOT"  


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
    
    assert check_device == None, "Device wasn't removed"  


def test_get_devices(timescaleDB):
    assert len(asdb.get_devices(1, timescaleDB)) == 3, "Number of devices is wrong, expected 3" 


def test_get_new_devices(timescaleDB):
    device_info = {
            'id': uuid.uuid4(),
            'place_id': 1, 
            'is_installed': False, 
            'name': 'New Device',
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

    devices = asdb.get_new_devices(timescaleDB)

    # remove new device for test to keep temp DB sustainable 
    timescaleDB.delete(devices[0])

    assert len(devices) == 1, "Number of new devices is wrong" 
    assert devices[0].place_id == device_info['place_id'], "Place ID is invalid"
    assert devices[0].is_installed == device_info['is_installed'], "Device is installed, expected NOT"
    assert devices[0].name == device_info['name'], "Device Name is wrong"   


def test_get_user_data(timescaleDB):
    test_query = asdb.get_user_data("test_user", db_session=timescaleDB)

    assert test_query.username == 'test_user', "No valid username"
    assert check_password_hash(test_query.password_hash, 'test_password'), "No valid password"


def test_create_user(timescaleDB):
    new_user = asdb.create_user(
        username='new_test_user', 
        password='new_test_password',
        db_session=timescaleDB
    )

    num_of_users = timescaleDB.query(User).count()
    # remove new user for test to keep temp DB sustainable 
    timescaleDB.delete(timescaleDB.query(User).get(2))
    
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


