import importlib 
import logging
import os
import sys 

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

# from models import metadata
from db import db 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d/%H:%M:%S')
logger = logging.getLogger(__name__)

def main():

    # db = SQLAlchemy(metadata=metadata)

    app = Flask(__name__)
    
    # only in dev mode! In prod => DEBUG = False!
    # Leaving it on will allow users to run 
    # arbitrary Python code on your server.
    app.config["DEBUG"] = True

    # If set to True, Flask-SQLAlchemy will track modifications 
    # of objects and emit signals. 
    # The default is None, which enables tracking but issues
    # a warning that it will be disabled by default in the future.
    # This requires extra memory and should be disabled if not needed.
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db_uri = os.getenv('DB_URI')
    if db_uri is None:
        logger.critical("MIGRATION MANAGER - DB_URI IS NOT FOUND")
        return 1
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    logger.debug(f"MIGRATION APP IS CONFIGURED SUCCESSFULLY: {db_uri}")

    db.init_app(app)

    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()
    
    return 0 

if __name__ == '__main__':
    sys.exit(main())