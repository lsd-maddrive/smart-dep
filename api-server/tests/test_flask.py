import os
import tempfile

from flask import Flask
import pytest

@pytest.fixture
def client():
    app = Flask(__name__)
    db = SQLAlchemy(metadata=metadata)

    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            flaskr.init_db() # ???????????????
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])