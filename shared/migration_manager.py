import os

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from models.table_models import db

app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG_OBJ'))

print(os.environ.get('CONFIG_OBJ'))

db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()