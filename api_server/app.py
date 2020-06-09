import logging
import os

from flask_login import LoginManager
from flask_restplus import Api
from flask_cors import CORS

from api_server.api_v1 import api as ns 
from api_server.api_func import create_app
from api_server.sockets import socketio
from api_server.database import db, load_user 


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()
db.init_app(app)
login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    logger.debug(f"Inside load_user func")
    return load_user(id)


socketio.init_app(app)

api = Api(app)
api.add_namespace(ns)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    socketio.run(app, debug=False, use_reloader=True)