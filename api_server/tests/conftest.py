import os
from datetime import datetime
import logging

# from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_cors import CORS
from pprint import pformat
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import testing.postgresql

from api_server.api_v1 import api as ns 
from api_server.api_func import create_app
from api_server.sockets import socketio
from db.models import Model, States 

from db.database import db 

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
        # None
    ]

    types = [
        'light', 
        'env', 
        'power'
        # 'unknown'
    ]

    states = []
    for type_ in types:
        for device in devices:
            states.append(
                States(
                    timestamp=datetime.now(), 
                    state= {'enabled': False}, 
                    device_id=device, 
                    place_id='8201', 
                    type=type_
                )
            )

    logger.debug(f"DB DATA STATES:\n{pformat(states)}")

    session.bulk_save_objects(
        objects=states
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
            