import os
# import sys 
# sys.path.append("../")
import tempfile

import pytest
from sqlalchemy import create_engine
import testing.postgresql

from db.models import * 

# from api_server.app import app, db  

# @pytest.fixture(scope='session')
# def client():
#     db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     app.config['TESTING'] = True

#     with app.test_client() as client:
#         with app.app_context():
#     #         flaskr.init_db() # ???????????????
#             pass
#         yield client

#     os.close(db_fd)
#     os.unlink(app.config['DATABASE'])


# or maybe scope='module' ??? 
# session - this fixture is visiable for every tests
# module - invoked once per module 
@pytest.fixture(scope='session')
def timescaleDB():
    db = testing.postgresql.Postgresql()
    engine = create_engine(db.url())
    Model.metadata.create_all(engine)

    # db = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)
   