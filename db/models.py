from flask_login import UserMixin
from sqlalchemy import MetaData, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB, BYTEA
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

metadata = MetaData() 
Model = declarative_base(metadata=metadata)

class Commands(Model):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    command = Column(JSONB)
    device_id = Column(String(50))
    place_id = Column(String(20))
    type = Column(String(10))

    def __repr__(self):
        return f"Command Type: {self.type}, Device ID: {self.device_id} \
                 DateTime: {self.timestamp}, Place ID: {self.place_id}"


class Configs(Model):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    config = Column(JSONB)
    device_id = Column(String(50))
    place_id = Column(String(20))
    type = Column(String(10))

    def __repr__(self):
        return f"Params Type: {self.type}, Device ID: {self.device_id} \
                 DateTime: {self.timestamp}, Place ID: {self.place_id}"


class States(Model):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    state = Column(JSONB)
    device_id = Column(String(20))
    place_id = Column(String(20))
    type = Column(String(10))

    def __repr__(self):
        return f"State Type: {self.type}, Device ID: {self.device_id} \
                 DateTime: {self.timestamp}, Place ID: {self.place_id}"
    
class Users(UserMixin, Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    password_hash = Column(String(128))
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    avatar_photo = Column(BYTEA)

    def __repr__(self):
        return f"User: {self.username}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ???????????????????????????????    
@login.user_loader
def load_user(id):
    return Users.query.get(int(id))