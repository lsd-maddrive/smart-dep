import os
import sys 
sys.path.append("..")

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from models.table_models import metadata

db = SQLAlchemy(metadata=metadata)

app = Flask(__name__)

env_mode = os.getenv('SMART_ENV', 'dev')
config_path = f'config/{env_mode}/config.py'

app.config.from_pyfile(config_path)

db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()