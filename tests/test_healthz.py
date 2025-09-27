import pytest
from fastapi.testclient import TestClient
from service.api import app


def test_healthz():
    client = TestClient(app)
    r = client.get('/healthz')
    assert r.status_code == 200
    assert r.json().get('ok') is True


def test_version():
    client = TestClient(app)
    r = client.get('/version')
    assert r.status_code == 200
    assert 'version' in r.json()
