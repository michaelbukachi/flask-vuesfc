import pytest
from flask import Flask
from flask.testing import FlaskClient


@pytest.fixture(scope='module')
def flask_app():
    app = Flask(__name__)
    app.config.update(SECRET_KEY='Some test')
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(flask_app):
    app = flask_app
    ctx = flask_app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()
