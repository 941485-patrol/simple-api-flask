import pytest
from app import app as app_test

@pytest.fixture
def app():
    yield app_test
@pytest.fixture
def client(app):
    yield app.test_client()