import importlib 
import logging
import os
import sys 
sys.path.append("..")

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from db.models.table_models import metadata

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)


db = SQLAlchemy(metadata=metadata)

app = Flask(__name__)

env_mode = os.getenv('SMART_ENV', 'dev')
config_path = f'config/{env_mode}/config.py'

app.config.from_pyfile(config_path)

app_config = importlib.import_module(f"config.{env_mode}.config")

logger.debug(f"Migration address: {app_config.SQLALCHEMY_DATABASE_URI}")

db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()