from datetime import datetime
import logging
import os
import sys 
sys.path.append("../")
import uuid

from flask_restplus import Api
from pprint import pformat
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import testing.postgresql
from werkzeug.security import generate_password_hash

from api_v1 import api as ns 
from api_func import create_app
from database import db 
from sockets import socketio
from db.models import Model, State, Device, Place, User

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def test_db():
    return testing.postgresql.Postgresql()

@pytest.fixture(scope='session')
def timescaleDB(request, test_db):
    engine = create_engine(test_db.url())
    logger.debug(f"Engine is created: {test_db.url()}")
    
    Model.metadata.create_all(engine)
    logger.debug('Create all models - done ')
    
    Session = sessionmaker(bind=engine)
    session = Session()
    logger.debug('session - done')
    
    types = [
        'light', 
        'env', 
        'power'
    ]


    place = Place(name='KEMZ', num='8201')

    session.add(place)
    session.commit() 

    logger.debug(f"Place is added to DB")

    place_id = session.query(Place).first().id 

    logger.debug(f"PLACE ID {place_id}")

    devices = []
    for i in range(3):
        devices.append(
            Device(
                place_id=place_id,
                register_date=datetime.now(), 
                is_installed=True, 
                type=types[i]
            )
    )

    session.bulk_save_objects(
        objects=devices
    )
    session.commit() 

    logger.debug(f"Devices are added to DB")

    devices_id = [device.id for device in session.query(Device).all()]

    states = []
    for i in range(3):
        states.append(
                State(
                    timestamp=datetime.now(), 
                    state= {'enabled': False}, 
                    device_id=devices_id[i], 
                )
            )
    
    session.bulk_save_objects(
        objects=states
    )
    session.commit()

    logger.debug(f"States are added to DB")
    
    test_user = User(username='test_user')
    test_user.password_hash = generate_password_hash('test_password')

    session.add(test_user)
    session.commit()

    logger.debug(f"User is added to DB")

    db_users = session.query(User).all()
    db_places = session.query(Place).all()
    db_devices = session.query(Device).all()
    db_states = session.query(State).all()

    logger.debug(
        f"DB DATA:\n" \
        f"Users\n{pformat(db_users)}\n" \
        f"Places\n{pformat(db_places)}\n" \
        f"Devices\n{pformat(db_devices)}\n" \
        f"States\n{pformat(db_states)}"
    )

    
    def resource_teardown():
        logger.debug("Database Resource teardown!")
        session.close()
        test_db.stop()
    request.addfinalizer(resource_teardown)

    return session


@pytest.fixture(scope='session')
def flask_app(test_db, timescaleDB):
    app = create_app(test_config=True)

    app.config['DATABASE'] = test_db.url()
    app.config["SQLALCHEMY_DATABASE_URI"] = test_db.url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['FLASK_DEBUG'] = False
    app.config['TESTING'] = True
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    app.config['SECRET_KEY'] = os.getenv('API_SECRET_KEY')

    logger.debug(f'Test App DB: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    db.init_app(app)

    socketio.init_app(app)
    api = Api(app)
    api.add_namespace(ns)

    return app


@pytest.fixture(scope='function')
def client(flask_app):
    with flask_app.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def sio_client(flask_app, client):
    sio_test_client = socketio.test_client(
        flask_app, flask_test_client=client
    )

    return sio_test_client
            