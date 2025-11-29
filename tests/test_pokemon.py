from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def get_pokemon() -> None:
    response = client.get("/api/pokemon")
    print(response)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2

def get_pokemon_id() -> None:
    response = client.get("/api/pokemon/1")
    print(response.json())
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 11
    assert content["id"] == 1

def get_pokemon_tipo() -> None:
    response = client.get(url="/api/pokemon/?tipo=4")
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 1

def get_pokemon_parte_nombre() -> None:
    response = client.get(url="/api/pokemon/?nombre_parcial=bul")
    assert response.status_code == 200
    content = response.json()