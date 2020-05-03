from sqlalchemy import MetaData, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData() 
Model = declarative_base(metadata=metadata)

class Commands(Model):
    __tablename__= 'commands'

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
    __tablename__= "configs"

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
    __tablename__= "states"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    state = Column(JSONB)
    device_id = Column(String(20))
    place_id = Column(String(20))
    type = Column(String(10))

    def __repr__(self):
        return f"State Type: {self.type}, Device ID: {self.device_id} \
                 DateTime: {self.timestamp}, Place ID: {self.place_id}"
    