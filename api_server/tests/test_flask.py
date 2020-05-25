import logging

import pytest

from db.models import * 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)

def test_db(timescaleDB):
    tmp = timescaleDB.query(States).all()
    logger.debug(f"Test query: {tmp}")

    for t in tmp:
        print("FIXTURE ")
        print(f"{t.state}")
        print(f"{t}")

    assert True
