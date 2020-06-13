from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session
from datetime import datetime

from db.models import metadata, States, Place, Device

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

### Places

def get_places(db_session=db.session):
    return db_session.query(Place).all()


def create_place(place_info, db_session=db.session):
    place = Place(
        name=place_info['name'],
        num=place_info['num'],
        create_date=datetime.utcnow()
    )

    db_session.add(place)
    db_session.commit()

    return place


def update_place(place_info, db_session=db.session):
    place = db_session.query(Place).get(place_info['id'])

    place.name = place_info['name']
    place.num = place_info['num']
    place.update_date = datetime.utcnow()

    db_session.commit()


def delete_place(place_info, db_session=db.session):
    place = db_session.query(Place).get(place_info['id'])

    db_session.delete(place)
    db_session.commit()

### Devices

def update_device(device_info, db_session=db.session):
    device = db_session.query(Device).get(device_info['id'])

    device.is_installed = True
    device.update_date = datetime.utcnow()

    device.name = device_info['name']
    device.type = device_info['type']
    device.place_id = device_info['place_id']
    device.config = device_info['config']

    db_session.commit()

def delete_device(device_info, db_session=db.session):
    device = db_session.query(Device).get(device_info['id'])

    if device.is_installed:
        device.update_date = datetime.utcnow()
        device.is_installed = False
        device.type = None
        device.place_id = None
        device.config = None
    else:
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
