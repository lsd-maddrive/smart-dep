from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class Commands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    command = db.Column(JSONB)
    device_id = db.Column(db.String(20))
    place_id = db.Column(db.String(20))
    type = db.Column(db.String(10))

    def __repr__(self):
        return f"Command Type: {self.type}, Device ID: {self.device_id} \
                 DateTime: {self.timestamp}, Place ID: {self.place_id}"


class Params(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    params = db.Column(JSONB)
    device_id = db.Column(db.String(20))
    place_id = db.Column(db.String(20))
    type = db.Column(db.String(10))

    def __repr__(self):
        return f"Params Type: {self.type}, Device ID: {self.device_id} \
                 DateTime: {self.timestamp}, Place ID: {self.place_id}"


class States(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    state = db.Column(JSONB)
    device_id = db.Column(db.String(20))
    place_id = db.Column(db.String(20))
    type = db.Column(db.String(10))

    def __repr__(self):
        return f"State Type: {self.type}, Device ID: {self.device_id} \
                 DateTime: {self.timestamp}, Place ID: {self.place_id}"
    