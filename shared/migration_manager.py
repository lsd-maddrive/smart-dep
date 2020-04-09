import os

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

# import environment_manager.py
from models.table_models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config["DEBUG"] = os.getenv("DEBUG")

print(os.getenv("SQLALCHEMY_DATABASE_URI"))
print(os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS"))
print(os.getenv("DEBUG"))

db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()