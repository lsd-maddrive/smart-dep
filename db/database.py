from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from models import * 

db = SQLAlchemy(metadata=metadata)

def get_last_states(check_time, place_id, type_):
    """
        Get last states from DB in defined period of time 
        from check time till now for defined place and type


        Args:
            check_time (datetime): the lower bound of time
            place_id (str): number/name of place 
            type_ (str): type of interaction [light, env, power]

        Returns:
            Query object that containts unique data for each
            device in defined period of time
    """
    return db.session.query(States). \
           filter(States.timestamp >= check_time). \
           filter(States.place_id == place_id). \
           filter(States.type == type_). \
           order_by(States.device_id, States.timestamp.desc()). \
           distinct(States.device_id)

def get_last_places(check_time):
    """
        Get last place ID from DB in defined period of time 
        from check time till now

        Args:
            check_time (datetime): the lower bound of time

        Returns:
            Query object that containts unique place id
    """
    return db.session.query(States.place_id). \
           filter(States.timestamp < check_time). \
           order_by(States.place_id, States.timestamp.desc()). \
           distinct(States.place_id)