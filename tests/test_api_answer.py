from fastapi.testclient import TestClient
from service.api import app


def test_answer_green():
    client = TestClient(app)
    r = client.post('/v1/answer', json={
        'query': 'what is the sterile changeover checklist?',
        'user_role': 'Operator'
    })
    data = r.json()
    assert r.status_code == 200
    assert data['lane'] == 'green'
    assert data['answer']


def test_answer_yellow():
    client = TestClient(app)
    r = client.post('/v1/answer', json={
        'query': 'where is the gowning table?',
        'user_role': 'Visitor'
    })
    data = r.json()
    assert r.status_code == 200
    assert data['lane'] == 'yellow'
    assert 'Advisory' in data['answer']

