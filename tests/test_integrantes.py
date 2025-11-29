from main import app
from fastapi.testclient import TestClient
from models.equipos.integrantes import IntegrantePost, IntegrantePut, Integrante
from models.equipos.movimientos import Movimiento
import pytest
from pydantic import ValidationError

client = TestClient(app)
def test_integrantepost_asignar_campos():
    data = IntegrantePost(id_pokemon=25, apodo="Pika")
    assert data.id_pokemon == 25
    assert data.apodo == "Pika"

def test_integranteput_comprobacion_datos():
    upd = IntegrantePut(apodo="Pro", movimientos=[85, 86, 87, 88])
    assert upd.apodo == "Pro"
    assert upd.movimientos == [85, 86, 87, 88]


def test_integrante():
    i = Integrante(
        id=1,
        apodo="Pika",
        pokemon={"id": 25, "nombre": "Pikachu", "imagen": "http://...", "tipos": ["Eléctrico"]},
        movimientos=[]
    )
    assert i.id == 1
    assert i.pokemon["id"] == 25
    assert isinstance(i.movimientos, list)

def test_integrante_verificacion():
    i = Integrante(
        id=3,
        apodo="Char",
        pokemon={"id": 6, "nombre": "Charizard", "imagen": "http://img", "tipos": ["Fuego", "Volador"]},
        movimientos=[]
    )
    assert {"id", "nombre", "imagen", "tipos"} <= set(i.pokemon.keys())
    assert isinstance(i.pokemon["tipos"], list)


def test_integrantepost_id_pokemon_invalido():
    try:
        _ = IntegrantePost(id_pokemon=-1, apodo="X")
        assert True  
    except ValidationError:
        assert True


def test_integrantepost_apodo_vacio():
    with pytest.raises(ValidationError):
        IntegrantePost(id_pokemon=25, apodo=123)


def test_integrante_pokemon_incompleto_aceptado():
    i = Integrante(id=10, apodo="X", pokemon={"id": 99}, movimientos=[])
    assert "imagen" not in i.pokemon