from datetime import datetime, timedelta
import logging

import pytest

import api_server.database as asdb
from db.models import States, User, Token

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)


def test_get_last_states(timescaleDB):
    _ = timescaleDB.query(States). \
                    filter(States.type == 'light'). \
                    order_by(States.device_id)
    # to store expected rows 
    right_states = []
    for right_state in _:
        right_states.append(right_state)

    test_query = asdb.get_last_states(
        check_time=datetime.now() - timedelta(minutes=5),
        place_id='8201', 
        type_='light', 
        db_session=timescaleDB
    )
    db_last_states = []
    for test_state in test_query:
        db_last_states.append(test_state)

    assert right_states == db_last_states 


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
    _ = timescaleDB.query(States). \
        order_by(States.device_id). \
        distinct(States.device_id)
    
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


