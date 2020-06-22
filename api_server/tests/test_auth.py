import logging
import sys 
sys.path.append("../")

import pytest

import auth as auth
import database as asdb
from db.models import Token

def test_decode_token(timescaleDB, flask_app):
    if timescaleDB.query(Token).count() == 0:
        new_token = asdb.save_token(
            user_id=1, 
            secret=flask_app.config['LOGIN_ENABLED'],
            db_session=timescaleDB
        )
    else:
        new_token = timescaleDB.query(Token).first()

    user_id, time = auth.decode_token(
        token=new_token.token,
        secret=flask_app.config['LOGIN_ENABLED']
    )

    # clear Token table to avoid conflicts in other tests
    asdb.delete_token(
        user_id=new_token.parent_id, 
        created_on=new_token.created_on,
        db_session=timescaleDB
    )

    assert user_id == 1, "User ID is wrong" 
