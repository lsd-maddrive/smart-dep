# import os 

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.ext.declarative import declarative_base 
# from sqlalchemy.orm import scoped_session, sessionmaker

# from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session
# from sqlalchemy.sql.expression import func

from models import * 

db = SQLAlchemy(metadata=metadata)

def get_last_states(check_time, place_id, type_):
    return db.session.query(States). \
           filter(States.timestamp >= check_time). \
           filter(States.place_id == place_id). \
           filter(States.type == type_). \
           order_by(States.device_id, States.timestamp.desc()). \
           distinct(States.device_id)

def get_last_places(check_time):
    return db.session.query(States.place_id). \
           filter(States.timestamp < check_time). \
           order_by(States.place_id, States.timestamp.desc()). \
           distinct(States.place_id)