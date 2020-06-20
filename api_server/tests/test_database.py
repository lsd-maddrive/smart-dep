from datetime import datetime, timedelta
import logging
from pprint import pformat

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

def test_get_last_places(timescaleDB):
    test_query = asdb.get_last_places(
        check_time=datetime.now() - timedelta(minutes=5),
        db_session=timescaleDB
    )
    db_last_places = []
    for test_place in test_query:
        db_last_places.append(test_place.place_id)

    # array for future modifications 
    assert db_last_places == ['8201']


def test_get_devices_states(timescaleDB):
    # the query is not stable if DB will be changed
    _ = timescaleDB.query(State). \
        order_by(State.device_id). \
        distinct(State.device_id)
    
    right_devices = []
    for right_device in _:
        right_devices.append(right_device)

    test_query = asdb.get_devices_states(
        check_time=datetime.now() - timedelta(minutes=5),
        db_session=timescaleDB
    )

    db_last_devices = []
    for test in test_query:
        db_last_devices.append(test)
    
    assert db_last_devices == right_devices


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


