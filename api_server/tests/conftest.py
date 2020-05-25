from datetime import datetime
import logging

from pprint import pformat
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import testing.postgresql

from db.models import * 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def timescaleDB(request):
    test_db = testing.postgresql.Postgresql()
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
                    state= {'enable': False}, 
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
        logger.debug("Resource teardown!")
        session.close()
        test_db.stop()
    request.addfinalizer(resource_teardown)

    return session