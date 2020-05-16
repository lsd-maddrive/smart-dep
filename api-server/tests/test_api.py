import sys 
sys.path.append("..")
import datetime


import logging
import requests 
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.models import metadata, Commands, Configs, States

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


db_uri = 'postgresql+psycopg2://admin:admin@localhost:5432/smart_dep'

# engine = None
# session = None

# if db_uri is None:
    # logger.critical('DB URI IS NOT FOUND')
# else:
engine = create_engine(db_uri)
session = Session(engine)
logger.debug("DB session is created successfully!")

current_timestamp = datetime.datetime.now()
time_delta = datetime.timedelta(minutes=5)
check_time = current_timestamp - time_delta

logger.debug(f"CHECK TIMESTAMP: {check_time}")

query = session.query(States). \
        filter(States.timestamp < check_time). \
        filter(States.place_id.like('8201')). \
        order_by(States.timestamp.desc()). \
        limit(5)
        # filter(States.timestamp >= check_time). \
        
        
        # order_by(States.timestamp.desc()). \
        # distinct(). \

for q in query:
    logger.debug(f"{q}\n")


# test light unit in api_v1.py 
# r = requests.get('http://localhost:5000/api/v1/place/8201/lights')