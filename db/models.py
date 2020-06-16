from pprint import pformat
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


metadata = MetaData()
Model = declarative_base(metadata=metadata)


class Command(Model):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    command = Column(JSONB)
    device_id = Column(ForeignKey("devices.id"))
    source_id = Column(String(50))

    device = relationship('Device')

    def __repr__(self):
        return f"Command | Device ID: {self.device_id}, DateTime: {self.timestamp}, Cmd: {self.command}, SID: {self.source_id}"


class Config(Model):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    config = Column(JSONB)
    device_id = Column(ForeignKey("devices.id"))

    device = relationship('Device')

    def __repr__(self):
        return f"Params | Device ID: {self.device_id}, DateTime: {self.timestamp}, Cfg: {self.config}"


class State(Model):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    state = Column(JSONB)
    device_id = Column(ForeignKey("devices.id"), nullable=False)

    device = relationship('Device')

    def get_did(self):
        return str(self.device_id)

    def __repr__(self):
        return f"State | Device ID: {self.device_id}, DateTime: {self.timestamp}, State: {self.state}"


class Place(Model):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    num = Column(String(20))
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    attr_os = Column(ARRAY(String(20)), default=[])
    attr_software = Column(ARRAY(String(20)), default=[])
    attr_people = Column(Integer, default=10)
    attr_computers = Column(Integer, default=25)
    attr_blackboard = Column(Boolean, default=False)
    attr_projector = Column(Boolean, default=False)

    # back_populates - refers to member of another class
    devices = relationship("Device", back_populates="place")

    def __repr__(self):
        return f"Place | ID: {self.id}, Name: {self.name}, Num: {self.num}"


class Device(Model):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"))
    register_date = Column(DateTime, nullable=False)
    enabled_date = Column(DateTime)
    update_date = Column(DateTime)
    ip_addr = Column(String(20))
    unique_id = Column(String(50), unique=True, nullable=True)
    type = Column(String(20))
    controller_type = Column(String(50))
    code_version = Column(String(20))
    is_installed = Column(Boolean, default=False)
    unit_config = Column(JSONB)

    # Custimization
    name = Column(String(50))
    icon_name = Column(String(50))

    place = relationship("Place", back_populates="devices")
    last_state = relationship(
        "State", order_by=State.timestamp.desc(), lazy='dynamic')

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"Device | ID: {self.id}, UID: {self.unique_id}, PlaceID: {self.place_id}, \
            RegDate: {self.register_date}, IP: {self.ip_addr}, Type: {self.type}, \
            Installed: {self.is_installed}, Config: {self.unit_config}"


class User(Model):
    """
        Users Model for storing users data
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime)
    avatar_photo = Column(BYTEA)
    role = Column(String(20))

    children = relationship("Token")

    def __init__(self, username, role='guest', avatar_photo=None):
        self.username = username
        self.created_on = datetime.now()
        self.role = role
        self.avatar_photo = avatar_photo

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User ID: {self.id}, Username: {self.username}, \
            Created Date: {self.created_on}, Role: {self.role}"


class Token(Model):
    """
        Token Model for storing valid JWT tokens
    """
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String(500), unique=True, nullable=False)
    created_on = Column(DateTime, nullable=False)
    expired_on = Column(DateTime, nullable=False)

    def __init__(self, parent_id, days, secs):
        self.parent_id = parent_id
        self.created_on = datetime.utcnow()
        self.expired_on = datetime.utcnow() + timedelta(days=days, seconds=secs)

    def __repr__(self):
        return f"ID: {self.id}, User ID: {self.parent_id}, \
            Creation Date: {self.created_on}, Expiration Date: {self.expired_on}"
