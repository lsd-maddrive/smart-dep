from sqlalchemy import MetaData, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base

import uuid

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


class Place(Model):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    num = Column(String(20))
    create_date = Column(DateTime)
    update_date = Column(DateTime)

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

    def __repr__(self):
        return f"Device | ID: {self.id}, UID: {self.unique_id}, PlaceID: {self.place_id}, RegDate: {self.register_date}, IP: {self.ip_addr}, Type: {self.type}, Installed: {self.is_installed}, Config: {self.config}"
