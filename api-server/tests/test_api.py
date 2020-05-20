import sys 
sys.path.append("..")
import datetime


import logging
import requests 
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from db.models import metadata, Commands, Configs, States

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


db_uri = 'postgresql+psycopg2://admin:admin@localhost:5432/smart_dep'

# engine = create_engine(db_uri)#, echo=True)
# session = Session(engine)

# current_timestamp = datetime.datetime.now()
# time_delta = datetime.timedelta(minutes=5)
# check_time = current_timestamp - time_delta

# tmp = session.query(States). \
#         filter(States.timestamp < check_time). \
#         filter(States.place_id == '8201'). \
#         filter(States.type == 'light'). \
#         order_by(States.device_id, States.timestamp.desc()). \
#         distinct(States.device_id)

# for t in tmp:
#     print(f"{t.state}\t{type(t.state)}")


# test light unit in api_v1.py 
r = requests.get('http://localhost:5000/api/v1/place/8201/powers')
r = requests.get('http://localhost:5000/api/v1/place/8201/lights')