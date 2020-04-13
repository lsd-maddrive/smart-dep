import os

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from models.table_models import db

app = Flask(__name__)

env_mode = os.environ.get('SMART_ENV')
if env_mode == 'test':
    config_path = 'config/test/config.py'
elif env_mode == 'prod':
    config_path = 'config/prod/config.py'
elif env_mode == 'dev':
    config_path = 'config/dev/config.py'
else: # in other cases - dev mode 
    config_path = 'config/dev/config.py'

app.config.from_pyfile(config_path)

db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()