import pytest
from unittest.mock import Mock, MagicMock
from fastapi.testclient import TestClient
from main import app
from database.api_busqueda_movimientos import MovimientosPedir
from fastapi import status
from dependencies.dependencies import inyectar_datamovimiento

mock_data_movimiento = MagicMock(MovimientosPedir)

MOVIMIENTO_COMPLETO = {
    "id": 32,
    "nombre": "Perforador",
    "tipo": {"id": 1, "nombre": "Normal"},
    "categoria": "físico",
    "potencia": 0,
    "precision": 30,
    "usos": 5,
    "efecto": "Causes a one-hit KO.",
    "pokemon_por_huevo": [
        {
            "id": 32,
            "imagen": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/32.png",
            "nombre": "nidoran-m",
            "altura": 0.5,
            "peso": 9.0,
        }
    ],
    "pokemon_por_nivel": [
        {
            "id": 33,
            "imagen": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/33.png",
            "nombre": "nidorino",
            "altura": 0.9,
            "peso": 19.5,
        },
    ],
    "pokemon_por_maquina": [
        {
            "id": 30,
            "imagen": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/30.png",
            "nombre": "nidorina",
            "altura": 0.8,
            "peso": 20.0,
        },
    ],
}

MOVIMIENTO_SIMPLE_BASE = {
    "id": 32,
    "nombre": "Perforador",
    "tipo": {"id": 1, "nombre": "Normal"},
    "categoria": "físico",
    "potencia": 0,
    "precision": 30,
    "usos": 5,
    "efecto": "Causes a one-hit KO.",
}

LISTA_MOVIMIENTOS = [
    MOVIMIENTO_SIMPLE_BASE,
    {
        "id": 33,
        "nombre": "Golpe",
        "tipo": {"id": 2, "nombre": "Lucha"},
        "categoria": "físico",
        "potencia": 70,
        "precision": 100,
        "usos": 20,
        "efecto": "Golpea.",
    },
]

ERROR_404 = {"detail": "Movimiento no encontrado"}


@pytest.fixture
def client():
    app.dependency_overrides[inyectar_datamovimiento] = lambda: mock_data_movimiento
    return TestClient(app)


def test_list_movimientos(client):
    mock_data_movimiento.obtener_todos_movimientos_db.reset_mock()
    mock_data_movimiento.obtener_todos_movimientos_db.return_value = LISTA_MOVIMIENTOS

    response = client.get("/movimientos/")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == len(LISTA_MOVIMIENTOS)
    assert content[0]["id"] == 32
    assert "pokemon_por_huevo" not in content[0]


def test_show_movimiento_ok(client):
    mock_data_movimiento.obtener_movimiento_id_db.reset_mock()
    mock_data_movimiento.obtener_movimiento_id_db.return_value = MOVIMIENTO_COMPLETO

    response = client.get("/movimientos/32")

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["id"] == 32
    assert content["nombre"] == "Perforador"
    assert "pokemon_por_huevo" in content
    assert len(content["pokemon_por_huevo"]) > 0


def test_show_movimiento_no_encontrado(client):
    mock_data_movimiento.obtener_movimiento_id_db.reset_mock()
    mock_data_movimiento.obtener_movimiento_id_db.return_value = None

    response = client.get("/movimientos/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == ERROR_404
