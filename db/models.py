from sqlalchemy import MetaData, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base

import uuid

metadata = MetaData()
Model = declarative_base(metadata=metadata)


class Command(Model):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    command = Column(JSONB)
    device_id = Column(ForeignKey("devices.id"))

    def __repr__(self):
        return f"Command | Device ID: {self.device_id}, DateTime: {self.timestamp}, Cmd: {self.command}"


class Config(Model):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    config = Column(JSONB)
    device_id = Column(ForeignKey("devices.id"))

    def __repr__(self):
        return f"Params | Device ID: {self.device_id}, DateTime: {self.timestamp}, Cfg: {self.config}"

class State(Model):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    state = Column(JSONB)
    device_id = Column(ForeignKey("devices.id"), nullable=False)

    device = relationship('Device')

    def get_did(self):
        return str(self.device_id)

    def __repr__(self):
        return f"State | Device ID: {self.device_id}, DateTime: {self.timestamp}, State: {self.state}, Device: {self.device}"


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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"))
    register_date = Column(DateTime, nullable=False)
    enabled_date = Column(DateTime)
    update_date = Column(DateTime)
    ip_addr = Column(String(20))
    unique_id = Column(String(50), unique=True, nullable=True)
    name = Column(String(50))
    type = Column(String(20))
    is_installed = Column(Boolean, default=False)
    config = Column(JSONB)

    place = relationship("Place", back_populates="devices")

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"Device | ID: {self.id}, UID: {self.unique_id}, PlaceID: {self.place_id}, RegDate: {self.register_date}, IP: {self.ip_addr}, Type: {self.type}, Installed: {self.is_installed}, Config: {self.config}"
