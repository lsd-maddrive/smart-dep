from datetime import datetime, timedelta
import logging
import os
from pprint import pformat

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import jwt
from pprint import pformat
from sqlalchemy import MetaData, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB, BYTEA
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

metadata = MetaData() 
Model = declarative_base(metadata=metadata)

class Commands(Model):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
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
    timestamp = Column(DateTime)
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
    timestamp = Column(DateTime)
    state = Column(JSONB)
    device_id = Column(String(20))
    place_id = Column(String(20))
    type = Column(String(10))

    def __repr__(self):
        return f"State Type: {self.type}, Device ID: {self.device_id},\
DateTime: {self.timestamp}, Place ID: {self.place_id}, State: {pformat(self.state)}"
    
class Users(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(128))
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime)
    avatar_photo = Column(BYTEA)
    role = Column(String(20))
    token = Column(String)


    def __init__(self, username, role='guest'):
        self.username = username
        # self.password_hash = self.set_password(password)
        self.created_on = datetime.now()
        self.role = role
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
        """
            Generates the Auth Token
            :return: string
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
                'exp': datetime.utcnow() + timedelta(days=0, seconds=30),
                # the time the token is generated
                'iat': datetime.utcnow(),
                # user who receive the token 
                'user': user_id
            }
            
            auth_token = jwt.encode(
                payload,
                os.getenv('API_SECRET_KEY'),
                algorithm='HS256'
            )
            # convert from bytes to string 
            return auth_token.decode('utf-8')
       
        except Exception as err:
            logger.error(f"Encode Token Payload Error {err}")
            return err

    @staticmethod
    def decode_auth_token(auth_token):
        """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, os.getenv('API_SECRET_KEY'), algorithms=['HS256'])
            # return user_id ?????????????????
            logger.debug(f"AFTER PAYLOAD: {payload}")
            return payload['user']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return f"User ID: {self.id}, Username: {self.username}, Created Date: {self.created_on}, Role: {self.role}\nHASH: {self.password_hash}"


class BlacklistToken(Model):
    """
        Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(500), unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return f"<id: {self.id} token: {self.token}"
