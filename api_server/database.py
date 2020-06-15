from db.models import metadata, State, Command, Config, Place, Device
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session
from datetime import datetime

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


db = SQLAlchemy(metadata=metadata)


def get_last_states(start_ts, place_id, db_session=db.session):
    """
        Get last states from DB in defined period of time
        from check time till now for defined place and type
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

# Places


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
        attr_people=place_info['attr_computers'],
        attr_computers=place_info['attr_people'],
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

# Devices


def update_device(device_info, db_session=db.session):
    device = db_session.query(Device).get(device_info['id'])

    device.is_installed = True
    device.update_date = datetime.utcnow()

    device.name = device_info['name']
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
