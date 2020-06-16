import logging

import pytest

import api_server.auth as auth
import api_server.database as asdb
from db.models import Token

def test_decode_token(timescaleDB, flask_app):
    if timescaleDB.query(Token).count() == 0:
        new_token = asdb.save_token(
            user_id=1, 
            secret=flask_app.config['SECRET_KEY'],
            db_session=timescaleDB
        )
    else:
        new_token = timescaleDB.query(Token).first()

    user_id, time = auth.decode_token(
        token=new_token.token,
        secret=flask_app.config['SECRET_KEY']
    )

    # clear Token table to avoid conflicts in other tests
    asdb.delete_token(
        user_id=new_token.parent_id, 
        created_on=new_token.created_on,
        db_session=timescaleDB
    )

    assert user_id == 1, "User ID is wrong" 
