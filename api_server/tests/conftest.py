from datetime import datetime
import logging

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
    
    test_state = States(
        timestamp=datetime.now(), 
        state= {'enabled': False}, 
        device_id='11:11:11:11:11:11',
        place_id='8201',
        type='light'
    )
    logger.debug(f"Test row: {test_state}")
    session.add(test_state)
    logger.debug("Test row - added")
    session.commit()
    logger.debug("Test row - commited")

    def resource_teardown():
        logger.debug("resource_teardown")
        session.close()
        test_db.stop()
    request.addfinalizer(resource_teardown)

    return session