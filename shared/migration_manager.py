import os
import sys 

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


def set_env(argv):
    if argv == 'test':
        env_path = Path('../testing') /'.env.test'
    elif argv == 'dep':
        # TO DO path to .env.dep
        pass

    return env_path
        

load_dotenv(dotenv_path=set_env(sys.argv[1]))

app = Flask(__name__)
# set_env(sys.argv[1])
print(os.getenv("SQLALCHEMY_DATABASE_URI"))
