from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_crear_equipo_ok() -> None:
    r = client.post("/api/equipos/", json={"nombre": "Z"})
    print(r.json())
    assert r.status_code == 201
    body = r.json()
    id_eqp = body["id"]
    assert body["nombre"] == "Z"
    assert body["integrantes"] == []
    r1 = client.delete(f"/api/equipos/{id_eqp}")
    body1 = r1.json()
    assert r1.status_code == 200
    assert body1["nombre"] == 'Z'


def test_crear_equipo_duplicado():
    r1 = client.post("/api/equipos", json={"nombre": "A"})
    r2 = client.post("/api/equipos", json={"nombre": "A"})
    assert r2.status_code == 400


def test_listar_equipos_ok():
    client.post("/api/equipos", json={"nombre": "B"})
    r = client.get("/api/equipos")
    assert r.status_code == 200
    assert all("cant_integrantes" in e for e in r.json())


def test_renombrar_y_eliminar():
    r = client.post("/api/equipos", json={"nombre": "C"})
    eid = r.json()["id"]
    r2 = client.put(f"/api/equipos/{eid}", json={"nombre": "C2"})
    assert r2.status_code == 200 and r2.json()["nombre"] == "C2"
    r3 = client.delete(f"/api/equipos/{eid}")
    assert r3.status_code == 200 and r3.json()["nombre"] == "C2"
