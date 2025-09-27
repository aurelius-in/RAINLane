from fastapi.testclient import TestClient
from service.api import app


def test_ingest_txt(tmp_path):
    p = tmp_path / 'sop.txt'
    p.write_text('SOP 4.2 Sterile Changeover ...')
    client = TestClient(app)
    r = client.post('/v1/ingest', json={'path': str(p)})
    data = r.json()
    assert r.status_code == 200
    assert 'doc_hash' in data and data['sections'] >= 1

