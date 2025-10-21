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
