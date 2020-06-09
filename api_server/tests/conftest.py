import os
from datetime import datetime
import logging

from flask_login import LoginManager
from flask_restplus import Api
from pprint import pformat
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import testing.postgresql

from api_server.api_v1 import api as ns 
from api_server.api_func import create_app
from api_server.database import db, load_user 
from api_server.sockets import socketio
from db.models import Model, States, Users

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
    
    devices = [
        '11:11:11:11:11:11', 
        '01:01:01:01:01:01', 
        'FF:FF:FF:FF:FF:FF'
    ]

    types = [
        'light', 
        'env', 
        'power'
    ]

    db_data = []

    for i in range(len(devices)):
        db_data.append(
                States(
                    timestamp=datetime.now(), 
                    state= {'enabled': False}, 
                    device_id=devices[i], 
                    place_id='8201', 
                    type=types[i]
                )
            )
    
    test_user = Users(
        username = "test_user", 
        created_on = datetime.now(), 
        updated_on = None, 
        avatar_photo = None,
        role = 'guest'
    )
    test_user.set_password("test_password")

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

    logger.debug(f'Test App DB: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        logger.debug(f"Inside TEST load_user func")
        return load_user(id)

    socketio.init_app(app)
    api = Api(app)
    api.add_namespace(ns)

    return app

@pytest.fixture(scope='session')
def login_manager(flask_app):
    login_manager = LoginManager(flask_app)
    login_manager.init_app(flask_app)

    @login_manager.user_loader
    def load_user(id):
        logger.debug(f"Inside TEST load_user func")
        return load_user(id)

    return login_manager





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
            