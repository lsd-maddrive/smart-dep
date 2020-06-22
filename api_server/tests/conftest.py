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
    logger.debug(f"Engine is creates: {test_db.url()}")
    
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


    db_data = [
        Place(
            name='KEMZ', 
            num='8201'
    )]
    
    # fixed place_id is OK, because other way will never happened
    for i in range(3):
        db_data.append(
            Device(
                id=uuid.uuid4(),
                place_id=1,
                register_date=datetime.now(), 
                is_installed=True, 
                type=types[i]
            )
    )

    for i in range(3):
        db_data.append(
                State(
                    timestamp=datetime.now(), 
                    state= {'enabled': False}, 
                    device_id=db_data[i+1].id, 
                )
            )
    
    test_user = User(username='test_user')
    test_user.password_hash = generate_password_hash('test_password')

    db_data.append(test_user)

    logger.debug(f"DB DATA STATES:\n{pformat(db_data)}")

    session.bulk_save_objects(
        objects=db_data
    )

    session.commit() 

    
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
    app.config['LOGIN_ENABLED'] = os.getenv('LOGIN_ENABLED')

    # logger.debug(f'Test App DB: {app.config["SQLALCHEMY_DATABASE_URI"]}')
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
            