
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Каждый тест по отдельности работает. Но вместе - ошибка  AttributeError: 'NoneType' object has no attribute 'send'.

def test_get_short_url():
    test_url = 'http://example.com'
    request_url = f'{app.url_path_for('get_short_url')}?url={test_url}'
    response = client.post(request_url)
    assert response.status_code == 201

def test_get_original_url():
    test_id = 'AOLK6Gw'
    response = client.get(app.url_path_for('get_original_url', url_id=test_id))
    assert response.status_code == 307

def test_get_original_url_error():
    test_id = 'errorID'
    response = client.get(app.url_path_for('get_original_url', url_id=test_id))
    assert response.status_code == 404

def test_get_status():
    test_id = 'AOLK6Gw'
    response = client.get(app.url_path_for('get_status', url_id=test_id))
    assert response.status_code == 200

def test_get_status_error():
    test_id = 'errorID'
    response = client.get(app.url_path_for('get_status', url_id=test_id))
    assert response.status_code == 404

def test_batch_upload_url():
    test_json = {
    "urls": [
        "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2_%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D1%8F_HTTP#302",
        "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2_%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D1%8F_HTTP#303",
        "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2_%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D1%8F_HTTP#304"
            ]
        }
    response = client.post(app.url_path_for('batch_upload_url'), json=test_json)
    assert response.status_code == 201


