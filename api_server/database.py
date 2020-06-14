from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from db.models import metadata, States, Users 

db = SQLAlchemy(metadata=metadata)

def get_last_states(check_time, place_id, type_, db_session=db.session):
    """
        Get last states from DB in defined period of time 
        from check time till now for defined place and type


        Args:
            check_time (datetime):   the lower bound of time
            place_id (str):          number/name of place 
            type_ (str):             type of interaction [light, env, power]
            db_session (sqlalchemy.orm.session.Session): session object  

        Returns:
            Query object that containts unique data for each
            device in defined period of time
    """
    return db_session.query(States). \
           filter(States.timestamp >= check_time). \
           filter(States.place_id == place_id). \
           filter(States.type == type_). \
           order_by(States.device_id, States.timestamp.desc()). \
           distinct(States.device_id)

def get_last_places(check_time, db_session=db.session):
    """
        Get last place ID from DB in defined period of time 
        from check time till now

        Args:
            check_time (datetime): the lower bound of time
            db_session (sqlalchemy.orm.session.Session): session object 

        Returns:
            Query object that containts unique place id
    """
    return db_session.query(States.place_id). \
           filter(States.timestamp >= check_time). \
           order_by(States.place_id, States.timestamp.desc()). \
           distinct(States.place_id)


def get_devices_states(check_time, db_session=db.session):
    """
        Get last states for all unique devices in defined 
        period of time 

        Args:
            check_time (datetime): the lower bound of time
            db_session (sqlalchemy.orm.session.Session): session object 
        
        Returns:
            Query object that containts data for each unique device
    """
    return db_session.query(States). \
           filter(States.timestamp >= check_time). \
           order_by(States.device_id, States.timestamp.desc()). \
           distinct(States.device_id)

# from api_server.app import login 
# ???????????????????????????????    
# @login.user_loader
def load_user(id, db_session=db.session):
    return db_session.query(Users).get(int(id))

def get_user_data(username, db_session=db.session):
    """
        Get all data about specified user

        Args: 
            username:   registered name of user 
            db_session (sqlalchemy.orm.session.Session): session object
        
        Returns: 
            Query object that contains data for ONE specified user (one row)
    """
    # BE CAREFULE, return sqlalchemy....result!!! 
    return db_session.query(Users). \
           filter(Users.username == username).first()


def create_user(username, password, db_session=db.session):
    if username is None or password is None:
        logger.critical(f"Username or password is missing")
        return -1 
    user = Users(
        username=username,
        password=password
    )
    logger.debug(f"User {user} - created")
    
    # user.set_password(password)
    logger.debug(f"User's password - set")

    db_session.add(user)
    logger.debug(f"User - added")
    db_session.commit()
    logger.debug(f"User - commited")

    logger.debug(f"User \"{username}\" is added to DB")

    return user 