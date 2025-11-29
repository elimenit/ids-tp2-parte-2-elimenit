from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_crear_equipo_ok():
    r = client.post("/api/equipos", json={"nombre": "Equipo Rocket"})
    assert r.status_code == 201
    body = r.json()
    assert body["nombre"] == "Equipo Rocket"
    assert body["integrantes"] == []


def test_crear_equipo_duplicado():
    client.post("/api/equipos", json={"nombre": "A"})
    client.post("/api/equipos", json={"nombre": "A"})
    r = client.post("/api/equipos", json={"nombre": "a"})
    assert r.status_code == 400
    assert r.json()["detalle"] == "Nombre de equipo duplicado"


def test_listar_equipos_ok():
    client.post("/api/equipos", json={"nombre": "B"})
    r = client.get("/api/equipos")
    assert r.status_code == 200
    assert all("cant_integrantes" in e for e in r.json())


def test_get_equipo_404():
    r = client.get("/api/equipos/9999")
    assert r.status_code == 404
    assert r.json()["detalle"] == "Equipo no encontrado"


def test_renombrar_y_eliminar():
    r = client.post("/api/equipos", json={"nombre": "C"})
    eid = r.json()["id"]
    r2 = client.put(f"/api/equipos/{eid}", json={"nombre": "C2"})
    assert r2.status_code == 200 and r2.json()["nombre"] == "C2"
    r3 = client.delete(f"/api/equipos/{eid}")
    assert r3.status_code == 200 and r3.json()["nombre"] == "C2"