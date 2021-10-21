import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_logout_path(client):
    rv = logout(client)
    assert b'You should be redirected automatically to target URL' in rv.data

def logout(client):
    return client.get('/logout')
