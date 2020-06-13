import time
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from models import metadata, States, Device

db = SQLAlchemy(metadata=metadata)


def commit(db_session=db.session):
    db_session.commit()


def set_device_enabled_info(unique_id, device_id, info, db_session=db.session):
    q = db_session.query(Device). \
        filter(Device.id == device_id)

    if unique_id is not None:
        q.filter(Device.unique_id == unique_id)

    device = q.one_or_none()
    if device is None:
        return None

    if 'ip_addr' in info:
        device.ip_addr = info['ip_addr']
    device.enabled_date = datetime.utcnow()

    commit(db_session)

    return device


def get_devices_with_uid(unique_id, db_session=db.session):
    return db_session.query(Device). \
        filter(Device.unique_id == unique_id)


def register_device(unique_id, db_session=db.session):
    device = Device(
        unique_id=unique_id,
        register_date=datetime.utcnow()
    )

    db_session.add(device)
    return device


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
