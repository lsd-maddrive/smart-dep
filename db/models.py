from datetime import datetime, timedelta
import logging
from pprint import pformat

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from pprint import pformat
from sqlalchemy import MetaData, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, BYTEA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

metadata = MetaData() 
Model = declarative_base(metadata=metadata)

class Commands(Model):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    command = Column(JSONB)
    device_id = Column(String(50))
    place_id = Column(String(20))
    type = Column(String(10))

    def __repr__(self):
        return f"Command Type: {self.type}, Device ID: {self.device_id},\
DateTime: {self.timestamp}, Place ID: {self.place_id}, Command: {pformat(self.command)}"


class Configs(Model):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    config = Column(JSONB)
    device_id = Column(String(50))
    place_id = Column(String(20))
    type = Column(String(10))

    def __repr__(self):
        return f"Params Type: {self.type}, Device ID: {self.device_id},\
DateTime: {self.timestamp}, Place ID: {self.place_id}, Config: {pformat(self.config)}"


class States(Model):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    state = Column(JSONB)
    device_id = Column(String(20))
    place_id = Column(String(20))
    type = Column(String(10))

    def __repr__(self):
        return f"State Type: {self.type}, Device ID: {self.device_id},\
DateTime: {self.timestamp}, Place ID: {self.place_id}, State: {pformat(self.state)}"


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
