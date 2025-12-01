from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_mostrar_movimientos() -> None:
    r = client.get("/api/movimientos/1")
    body = r.json()
    assert r.status_code == 200
    assert body["id"] == 1

def test_todos_los_movimientos() -> None:
    r = client.get("/api/movimientos/", params={"limit": 50, "offset":0})
    body = r.json()
    assert r.status_code == 200
    assert len(body) == 50
