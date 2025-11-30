from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_crear_equipo_ok() -> None:
    r = client.post("/api/equipos", json={"nombre": "Vsffdf"})
    print(r.json())
    assert r.status_code == 201
    body = r.json()
    assert body["nombre"] == "Vsffdf"
    assert body["integrantes"] == []


def test_crear_equipo_duplicado():
    r1 = client.post("/api/equipos", json={"nombre": "A"})
    r2 = client.post("/api/equipos", json={"nombre": "A"})
    assert r2.status_code == 400
    print(r2.json()["detalle"])
    assert r2.json()["detalle"] == "Nombre de equipo duplicado"


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

def main():
    test_crear_equipo_ok()
    test_crear_equipo_duplicado()
    test_listar_equipos_ok()
    test_renombrar_y_eliminar()

main()