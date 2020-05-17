import sys 
sys.path.append("..")
import datetime


import logging
import requests 
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

engine = create_engine(db_uri)
session = Session(engine)

current_timestamp = datetime.datetime.now()
time_delta = datetime.timedelta(minutes=5)
check_time = current_timestamp - time_delta

# tmp = session.query(States.device_id, States.type, func.max(States.timestamp).label('last_time')). \
#         filter(States.type.like('light')). \
#         group_by(States.device_id)
    
# for t in tmp:
#     print(f"{t}")

# light_only_subquery = session.query(States, func.max(States.timestamp)). \
#                       filter(States.type == 'light'). \
#                       group_by(States.device_id)

# for los in light_only_subquery:
#     print(f"{los}")


last_states_subquery = session.query(States.device_id, States.type, func.max(States.timestamp).label('last_time')). \
                    group_by(States.device_id, States.type).subquery()

time_place_query = session.query(States). \
                   filter(States.timestamp < check_time). \
                   filter(States.place_id.like('8201')) #. \
                #    filter(States.type.like('light'))


# query = session.query(States, last_states.c.last_time). \
#         join( 
#             last_states, States.timestamp==last_states.c.last_time 
#         ).order_by(States.id)

result = time_place_query.join(
    last_states_subquery, States.timestamp==last_states_subquery.c.last_time 
).order_by(States.id)



# query = session.query(States). \
#         filter(States.timestamp < check_time). \
#         filter(States.place_id.like('8201')). \
#         all()


# query = session.query(States).join(
#     last_states, \
#     States.timestamp < check_time, \
#     States.place_id == '8201'
# ).order_by(last_states.timestamp.desc())


# query = session.query(States). \
#         filter(States.timestamp < check_time). \
#         filter(States.place_id.like('8201')). \
#         group_by(States.id, States.device_id). \
#         distinct()
# #         query(States.id, func.max(State.timestamp)). \
# #         group_by(States.device_id)
# #         # group_by(States.device_id)
# #         # filter(func.max(States.id))
# #         # distinct(States.device_id)

# #         # order_by(States.timestamp.desc()). \
# #         # limit(5)
# #         # filter(States.timestamp >= check_time). \
        
# # #         # order_by(States.timestamp.desc()). \
# # #         # distinct(). \

for q in result:
    logger.debug(f"{q}\n{q.state}")

# test light unit in api_v1.py 
# r = requests.get('http://localhost:5000/api/v1/place/8201/lights')