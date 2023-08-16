import pytest
from flask import Flask
from flask.testing import FlaskClient
from application.main import main  
from werkzeug.security import generate_password_hash, check_password_hash
from app import *
from application.models import User

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app


@pytest.fixture
def user_1():
    user_1 = User(name="Nounou", email="nounou@test.com",
                    password=generate_password_hash('nounou', method='sha256'))
    return user_1


@pytest.fixture
def user_2():
    user_2 = User(name="Chichi", email="chichi@test.com",
                    password=generate_password_hash('123', method='sha256'))
    return user_2


@pytest.fixture
def user_3():
    user_3 = User(name="Titi", email="titi@test.com",
                    password=generate_password_hash('123', method='sha256'))
    return user_3


def test_models(user_1, user_2, user_3):
    assert user_1.name == "Nounou"
    assert user_1.password != 'nounou'
    assert check_password_hash(user_1.password, 'nounou') == True
    assert user_2.name == "Chichi"
    assert user_2.password != '123'
    assert check_password_hash(user_2.password, '123') == True
    assert user_3.name == "Titi"
    assert user_3.password != '123'
    assert check_password_hash(user_3.password, '123') == True






