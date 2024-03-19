from fastapi.testclient import TestClient
from src.main import app


# Что-то не получается никак запустить тест. Ошибка 422.
client = TestClient(app)

response = client.post("/?url=http://example.com")
assert response.status_code == 201

