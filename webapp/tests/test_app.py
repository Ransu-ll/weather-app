import pytest
from webapp.app import app

@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Aussie's Weather Webapp" in resp.data

def test_correct_404_response(client):
    resp = client.get("/hello", follow_redirects=True)
    assert b"Page Not Found" in resp.data

def test_correct_400_response(client):
    resp = client.get("/town/hello", follow_redirects=True)
    assert b"Town Not Found" in resp.data