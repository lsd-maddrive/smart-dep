import os
import uuid
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy_utils import create_database, drop_database
# from yarl import URL
import testing.postgresql

from db.models import * 
# from api_server.app import app 

@pytest.fixture(scope='session')
def timescaleDB():
    db = testing.postgresql.Postgresql()
    engine = create_engine(db.url())
    session = sessionmaker(bind=engine)
    Model.metadata.create_all(engine)

    tmp = session.query(States).limit(2)
    for t in tmp:
        print("FIXTURE ")
        print(f"{t}")
    
    return db.url()
    

def test_db():

    db = testing.postgresql.Postgresql()
    engine = create_engine(db.url())
    Session = sessionmaker(bind=engine)
    session = Session()
    Model.metadata.create_all(engine)

    tmp = session.query(States).limit(2)
    for t in tmp:
        print("FIXTURE ")
        print(f"{t}")

    # tmp = timescaleDB.query(States).limit(2)
    # for t in tmp:
    #     print("FIXTURE ")
    #     print(f"{t}")

    assert True