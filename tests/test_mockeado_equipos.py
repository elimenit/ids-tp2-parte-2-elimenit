import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock

PATH_DB = "database.database"

from database.database import EquipoDB
from models.equipos.equipos import Equipo
from models.equipos.integrantes import (
    Integrante,
    IntegrantePost,
    IntegrantePut,
    IntegrantePostMovimiento,
)
from models.equipos.movimientos import Movimiento

@pytest.fixture
def equipo_db():
    """
    BD mínima para testear: 1 equipo (id=1, 'Team Rocket') con 1 integrante (id=1, 'PikaTeam').
    El Pokémon del integrante tiene tipo 13 (eléctrico) para poder validar tipos de movimientos.
    """
    db = EquipoDB(
        id_equipo=1,
        equipos=[
            Equipo(
                id=1,
                nombre="Team Rocket",
                integrantes=[
                    Integrante(
                        id=1,
                        apodo="PikaTeam",
                        pokemon={"id": 25, "tipos": [{"id": 13}]},
                        movimientos=[],
                    )
                ],
            )
        ],
        id_integrante=1,
        integrantes=[
            Integrante(
                id=1,
                apodo="PikaTeam",
                pokemon={"id": 25, "tipos": [{"id": 13}]},
                movimientos=[],
            )
        ],
    )
    return db


def test_edit_integrante_ok_capitaliza_y_vacia_movs(equipo_db):
    info = IntegrantePut(apodo="   PikaTeam   ", movimientos=[])
    intg = equipo_db.edit_integrante(1, 1, info)
    assert intg.apodo == "PikaTeam"
    assert intg.movimientos == []


def test_edit_integrante_apodo_duplicado_403(equipo_db):
    nuevo = Integrante(id=2, apodo="Miau", pokemon={"id": 1, "tipos": [{"id": 1}]}, movimientos=[])
    equipo_db.integrantes.append(nuevo)
    equipo_db.equipos[0].integrantes.append(nuevo)

    info = IntegrantePut(apodo="Miau", movimientos=[])
    with pytest.raises(HTTPException) as ex:
        equipo_db.edit_integrante(1, 1, info)
    assert ex.value.status_code == 403
    assert "ya existe" in ex.value.detail


def test_edit_integrante_mas_de_cuatro_movs_403(equipo_db):
    info = IntegrantePut(apodo="PikaTeam", movimientos=[1, 2, 3, 4, 5])
    with pytest.raises(HTTPException) as ex:
        equipo_db.edit_integrante(1, 1, info)
    assert ex.value.status_code == 403
    assert "no puede tener mas de 4 movimientos" in ex.value.detail


def test_edit_integrante_tipo_mov_no_concuerda_403(equipo_db):
    with patch(f"{PATH_DB}.obtener_type_id_movimiento", return_value=99):
        info = IntegrantePut(apodo="PikaTeam", movimientos=[85, 86])
        with pytest.raises(HTTPException) as ex:
            equipo_db.edit_integrante(1, 1, info)
        assert ex.value.status_code == 403
        assert "no coincide con ningún tipo del pokemon" in ex.value.detail


def test_edit_integrante_setea_movimientos_por_metodo_de_clase(equipo_db):
    fake_movs = [
        Movimiento(
            id=85, nombre="Trueno",
            tipo={"id": 13, "nombre": "eléctrico"},
            categoria="especial", potencia=110, precision=70, usos=10, efecto="golpea"
        )
    ]
    with (
        patch(f"{PATH_DB}.obtener_type_id_movimiento", return_value=13),
        patch.object(EquipoDB, "obtener_movimientos", return_value=fake_movs) as mock_get,
    ):
        info = IntegrantePut(apodo="PikaTeam", movimientos=[85])
        intg = equipo_db.edit_integrante(1, 1, info)
        assert intg.movimientos == fake_movs
        mock_get.assert_called_once_with([85])



def test_add_movimiento_integrante_ok(equipo_db):
    mov = Movimiento(
        id=85, nombre="Trueno",
        tipo={"id": 13, "nombre": "eléctrico"},
        categoria="especial", potencia=110, precision=70, usos=10, efecto="golpea"
    )
    with patch.object(EquipoDB, "obtener_movimientos", return_value=[mov]):
        out = equipo_db.add_movimiento_integrante(1, 1, IntegrantePostMovimiento(id_movimiento=85))
        assert out == mov
        assert equipo_db.equipos[0].integrantes[0].movimientos == [mov]


def test_add_movimiento_integrante_quinto_403(equipo_db):
    equipo_db.equipos[0].integrantes[0].movimientos = [MagicMock()] * 4
    with pytest.raises(HTTPException) as ex:
        equipo_db.add_movimiento_integrante(1, 1, IntegrantePostMovimiento(id_movimiento=1))
    assert ex.value.status_code == 403
    assert "ya tiene 4 movimientos" in ex.value.detail


def test_add_movimiento_integrante_tipo_invalido_403(equipo_db):
    bad = Movimiento(
        id=1, nombre="Placaje",
        tipo={"id": 1, "nombre": "normal"},
        categoria="físico", potencia=40, precision=100, usos=35, efecto="golpea"
    )
    with patch.object(EquipoDB, "obtener_movimientos", return_value=[bad]):
        with pytest.raises(HTTPException) as ex:
            equipo_db.add_movimiento_integrante(1, 1, IntegrantePostMovimiento(id_movimiento=1))
        assert ex.value.status_code == 403
        assert "no coincide con ningún tipo del pokemon" in ex.value.detail


def test_delete_integrante_ok(equipo_db):
    borrado = equipo_db.delete_integrante(1, 1)
    assert borrado.id == 1
    assert equipo_db.equipos[0].integrantes == []


def test_listar_integrantes_ok(equipo_db):
    lista = equipo_db.listar_integrantes(1)
    assert len(lista) == 1
    assert lista[0].apodo == "PikaTeam"


def test_obtener_movimientos_arma_objetos(equipo_db):
    with (
        patch(f"{PATH_DB}.obtener_type_id_movimiento", return_value=13),
        patch(f"{PATH_DB}.nombre_movimientos", return_value="Trueno"),
        patch(f"{PATH_DB}.nombre_tipo_id", return_value="eléctrico"),
        patch(f"{PATH_DB}.obtener_id_categoria", return_value="especial"),
        patch(f"{PATH_DB}.nombre_categoria", return_value="especial"),
        patch(f"{PATH_DB}.obtener_potencia", return_value=110),
        patch(f"{PATH_DB}.obtener_precision", return_value=70),
        patch(f"{PATH_DB}.obtener_usos", return_value=10),
        patch(f"{PATH_DB}.obtener_efecto_corto", return_value="golpea"),
    ):
        movs = equipo_db.obtener_movimientos([85])
        assert len(movs) == 1
        m = movs[0]
        assert isinstance(m, Movimiento)
        assert m.id == 85
        assert m.nombre == "Trueno"
        assert m.tipo == {"id": 13, "nombre": "eléctrico"}
        assert m.categoria == "especial"
        assert m.potencia == 110
        assert m.precision == 70
        assert m.usos == 10
        assert m.efecto == "golpea"

def test_obtener_pokemon_dict_normalizado(equipo_db):
    with (
        patch(f"{PATH_DB}.imagen_pokemon_id", return_value="img/025.png"),
        patch(f"{PATH_DB}.nombre_pokemon_id", return_value="PikaTeamchu"),
        patch(f"{PATH_DB}.obtener_types_id_pokemon_id", return_value=[13]), 
        patch(f"{PATH_DB}.tipos", return_value=[{"id": 13, "nombre": "eléctrico"}]),  
    ):
        p = equipo_db.obtener_pokemon(25)

        assert p["id"] == 25
        assert p["imagen"] == "img/025.png"
        assert p["nombre"] == "PikaTeamchu"
        assert p["tipos"] == [{"id": 13, "nombre": "eléctrico"}]

def test_add_integrante_ok(equipo_db):
    with patch.object(EquipoDB, "obtener_pokemon",
                      return_value={"id": 4, "tipos": [{"id": 10}]}):
        nuevo = equipo_db.add_integrante(1, IntegrantePost(id_pokemon=4, apodo="char"))
        assert nuevo.id == 2                     # autoincrementa desde 1
        assert nuevo.apodo == "Char"
        assert nuevo.pokemon["id"] == 4
        assert equipo_db.equipos[0].integrantes[-1].id == 2


def test_add_integrante_equipo_lleno_403(equipo_db):
    equipo_db.equipos[0].integrantes = [
        Integrante(id=i, apodo=f"X{i}", pokemon={"id": i, "tipos": [{"id": 1}]}, movimientos=[])
        for i in range(1, 7)
    ]
    with pytest.raises(HTTPException) as ex:
        equipo_db.add_integrante(1, IntegrantePost(id_pokemon=4, apodo="char"))
    assert ex.value.status_code == 403
    assert "ya tiene 6 integrantes" in ex.value.detail