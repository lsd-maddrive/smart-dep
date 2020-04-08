from datetime import datetime  
import os
import sys 
sys.path.append("../shared/models")

db_config_path = os.path.relpath('../config/sqlalchemy_config.py', os.path.dirname(__file__))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from table_models import db, Commands, Params, States 

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(db_config_path)
    db.init_app(app)
    return app

def add_new_row(table_obj):
    with app.app_context():
        db.session.add(table_obj)
        db.session.commit() 

if __name__ == "__main__":
    app = create_app()
    new_command = Commands(timestamp=datetime.now(), 
                           command={}, device_id="test1", 
                           place_id="8201", type="Power")
    add_new_row(new_command)