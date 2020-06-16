from datetime import datetime, timedelta
import logging
import os
from pprint import pformat

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import jwt
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


class Users(Model):
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
    
    children = relationship("Tokens")


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


class Tokens(Model):
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
    

    def encode_auth_token(self):
        """
            Generates the Auth Token
            Args:
                user_id(integer): parent ID 
            Returns: 
                token (string)
        """
        try:
            header = {
                'typ': 'JWT', 
                'alg': 'HS256'
            }

            payload = {
                # the subject of the token 
                'sub': "auth", 
                # expiration date of the token
                'exp': self.expired_on,
                # the time the token is generated
                'iat': self.created_on,
                # user who receive the token 
                'user': self.parent_id,
            }

            auth_token = jwt.encode(
                payload,
                os.getenv('API_SECRET_KEY'),
                algorithm=header['alg']
            )
            # convert from bytes to string 
            self.token = auth_token.decode('utf-8')
       
        except Exception as err:
            logger.error(f"Encode Token Payload Error {err}")
            return err

    @staticmethod
    def decode_auth_token(auth_token):
        """
            Decodes the auth token
            Args: 
                auth_token: encoded token (payload)
            Returns:
                user ID (integer)
                time of creation token (int) = number of seconds
        """
        try:
            payload = jwt.decode(auth_token, os.getenv('API_SECRET_KEY'), algorithms=['HS256'])
            return payload['user'], payload['iat']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.', ''
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.', ''

    def __repr__(self):
        return f"ID: {self.id}, User ID: {self.parent_id}, \
Creation Date: {self.created_on}, Expiration Date: {self.expired_on}"
