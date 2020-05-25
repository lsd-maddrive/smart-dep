from datetime import datetime, timedelta
import logging

import pytest

from db.database import * 
from db.models import States 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)


def test_db(timescaleDB):
    # right_states = 


    db_last_states = get_last_states(
        check_time=datetime.now() - timedelta(minutes=5),
        place_id='8201', 
        type_='light', 
        db_session=timescaleDB
    )

    logger.debug(f"TYPE: {type(db_last_states)}, {type(timescaleDB)}")

    
    assert True  