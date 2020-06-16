from datetime import datetime, timedelta
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from flask_sqlalchemy import SQLAlchemy
import jwt
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session

import api_server.auth as auth
from db.models import metadata, States, User, Token

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
    return db_session.query(User). \
           filter(User.username == username).first()


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
    user = User(username=username)
    user.set_password(password)
    
    db_session.add(user)
    db_session.commit()

    logger.debug(f"User \"{user}\" is added to DB")

    return user 


# TODO: maybe ser life time of token in another place (??)
def save_token(user_id, secret, db_session=db.session, exp_days=7, exp_sec=0):
    """
        Add new token-row to DB (Tokens table)

        Args: 
            user_id (int):   parent ID  
            exp_delta(datetime.timedelta): time delta for expiring token 
            db_session (sqlalchemy.orm.session.Session): session object
        
        Returns: 
            encoded token (string)
    """
    new_token = Token(parent_id=user_id, days=exp_days, secs=exp_sec)

    new_token.token = auth.encode_token(
        user_id=new_token.parent_id,
        created_time=new_token.created_on, 
        expired_time=new_token.expired_on,
        secret=secret
    )

    db_session.add(new_token)
    db_session.commit()

    logger.debug(f"New token {new_token} is saved")

    return new_token


def delete_token(user_id, created_on, db_session=db.session):
    if isinstance(created_on, int):
        created_on = datetime.utcfromtimestamp(created_on)

    db_session.query(Token). \
        filter(Token.parent_id == user_id). \
            filter(Token.created_on == created_on). \
                delete()
    
    db_session.commit()
    # TODO: fix time from utc to local time (?) only for info representation
    logger.debug(f"Token for User ID: {user_id} created: {created_on} was deleted")


