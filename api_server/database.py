from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from db.models import metadata, States, Users, Tokens#, BlacklistToken 

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
            username (string):   registered name of user 
            db_session (sqlalchemy.orm.session.Session): session object
        
        Returns: 
            Query object that contains data for ONE specified user (one row)
    """
    # BE CAREFULE, return sqlalchemy....result!!! 
    return db_session.query(Users). \
           filter(Users.username == username).first()


def find_user(user_id, db_session=db.session):
    return db_session.query(Users). \
        filter(Users.id == user_id).first() 


def create_user(username, password, db_session=db.session):
    """
        Add new user-row to DB (Users table)

        Args: 
            username:   name of user 
            password:   obviosly, password (not hashed yet)
            db_session (sqlalchemy.orm.session.Session): session object
        
        Returns: 
            Query object that contains data for new specified user (one row)
    """
    user = Users(username=username)
    user.set_password(password)
    
    db_session.add(user)
    db_session.commit()

    logger.debug(f"User \"{user}\" is added to DB")

    return user 


def save_token(user_id, db_session=db.session, exp_days=0, exp_sec=2):
    """
        Add new token-row to DB (Tokens table)

        Args: 
            user_id (int):   parent ID  
            exp_delta(datetime.timedelta): time delta for expiring token 
            db_session (sqlalchemy.orm.session.Session): session object
        
        Returns: 
            encoded token (string)
    """
    new_token = Tokens(parent_id=user_id, days=exp_days, secs=exp_sec)
    new_token.encode_auth_token()

    db_session.add(new_token)
    db_session.commit()

    logger.debug(f"New token {new_token} is saved")

    return new_token.token


def delete_token(user_id, created_on, db_session=db.session):
    db_session.query(Tokens). \
        filter(Tokens.parent_id == user_id). \
            filter(Tokens.created_on == datetime.utcfromtimestamp(created_on)).delete()
    
    db_session.commit()

    logger.debug(f"Token for User ID: {user_id} created: {datetime.utcfromtimestamp(created_on)} was deleted")

    
