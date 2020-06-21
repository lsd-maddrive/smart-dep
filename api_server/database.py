from datetime import datetime, timedelta
import logging
import os

from flask_sqlalchemy import SQLAlchemy
import jwt
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from sqlalchemy import desc
from werkzeug.security import generate_password_hash

import auth
from db.models import metadata, User, Token, State, Command, Config, Place, Device


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


db = SQLAlchemy(metadata=metadata)


def get_last_states(start_ts, place_id, db_session=db.session):
    """
        Get last states from DB in defined period of time
        from check time till now for defined place

        Args:
            start_ts (timestamp):    the lower bound of time
            place_id (str):          number/name of place
            db_session (sqlalchemy.orm.session.Session): session object
        Returns:
            Query object that containts unique data for each
            device in defined period of time
    """
    return db_session.query(State) \
        .filter(State.timestamp >= start_ts) \
        .filter(State.device.has(Device.place_id == place_id)) \
        .order_by(State.device_id, State.timestamp.desc()) \
        .distinct(State.device_id).all()


def get_places(db_session=db.session):
    return db_session.query(Place).all()


def create_place(place_info, db_session=db.session):
    place = Place(
        name=place_info['name'],
        num=place_info['num'],
        create_date=datetime.utcnow(),

        # TODO - use .get() with defaults
        attr_os=place_info['attr_os'],
        attr_software=place_info['attr_software'],
        attr_people=place_info['attr_people'],
        attr_computers=place_info['attr_computers'],
        attr_blackboard=place_info['attr_board'],
        attr_projector=place_info['attr_projector']
    )

    db_session.add(place)
    db_session.commit()

    return place


def update_place(place_info, db_session=db.session):
    place = db_session.query(Place).get(place_info['id'])

    place.name = place_info['name']
    place.num = place_info['num']
    place.update_date = datetime.utcnow()

    place.attr_os = place_info['attr_os']
    place.attr_software = place_info['attr_software']
    place.attr_people = place_info['attr_people']
    place.attr_computers = place_info['attr_computers']
    place.attr_blackboard = place_info['attr_board']
    place.attr_projector = place_info['attr_projector']

    db_session.commit()


def delete_place(place_info, db_session=db.session):
    place = db_session.query(Place).get(place_info['id'])

    db_session.delete(place)
    db_session.commit()


def update_device(device_info, db_session=db.session):
    device = db_session.query(Device).get(device_info['id'])

    device.is_installed = True
    device.update_date = datetime.utcnow()

    device.name = device_info['name']
    device.icon_name = device_info['icon_name']
    device.type = device_info['type']
    device.place_id = device_info['place_id']
    device.unit_config = device_info['config']

    db_session.commit()


def reset_device(device_info, db_session=db.session):
    # Moreover remove old data
    db_session.query(State) \
        .filter(State.device_id == device_info['id']).delete()
    db_session.query(Command) \
        .filter(Command.device_id == device_info['id']).delete()
    db_session.query(Config) \
        .filter(Config.device_id == device_info['id']).delete()

    db_session.flush()

    device = db_session.query(Device).get(device_info['id'])
    device.update_date = datetime.utcnow()
    device.is_installed = False
    device.type = None
    device.place_id = None
    device.unit_config = None

    db_session.commit()


def delete_device(device_info, db_session=db.session):
    # Moreover remove old data
    db_session.query(State) \
        .filter(State.device_id == device_info['id']).delete()
    db_session.query(Command) \
        .filter(Command.device_id == device_info['id']).delete()
    db_session.query(Config) \
        .filter(Config.device_id == device_info['id']).delete()

    db_session.flush()

    device = db_session.query(Device).get(device_info['id'])
    db_session.delete(device)

    db_session.commit()


def get_devices(place_id=None, db_session=db.session):
    q = db_session.query(Device) \
        .filter(Device.is_installed == True)

    if place_id is not None:
        q = q.filter(Device.place_id == place_id)

    return q.all()


def get_new_devices(db_session=db.session):
    return db_session.query(Device). \
        filter(Device.is_installed == False).all()


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
    user.password_hash = generate_password_hash(password)

    db_session.add(user)
    db_session.commit()

    logger.debug(f"User \"{user}\" is added to DB")

    return user


# TODO: maybe set lifetime of token in another place (??)
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
    logger.debug(
        f"Token for User ID: {user_id} created: {created_on} was deleted")


def save_place_image(id, img, db_session=db.session):
    place = db_session.query(Place). \
        filter(Place.id == id).first()
    
    place.image = img 
    
    # update row 
    db_session.commit()

    logger.debug(f"Image for Place ID {id} is saved successfully.")
    

def get_place_data(id, db_session=db.session):
    """
        Get all data of specified place 

        Args:
            id (int):   place id 
            db_session (sqlalchemy.orm.session.Session): session object

        Returns:
            place [1 row]

    """
    return db_session.query(Place). \
        filter(Place.id == id).first() 
