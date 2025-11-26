import pytest
from seeds.leer_archivos import LeerArchivos


def test_leer_moves(mocker):
    files = LeerArchivos()
    devolver = {
        1: ["movi_1", 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11],
        2: ["movi_2", 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11],
    }
    mocker.patch("seeds.leer_archivos.LeerArchivos.leer_moves", return_value=devolver)
    MV = files.leer_moves()
    assert isinstance(MV, dict)
    assert len(MV) == 2
    assert MV[1][0] == "movi_1"
    assert MV[2][0] == "movi_2"


def test_leer_move_damage_class_prose(mocker):
    files = LeerArchivos()
    devolver = {
        1: [
            [2],
            ["hola"],
            ["descripcion"],
        ],
        3: [
            [4],
            ["hola"],
            ["descripcion"],
        ],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_move_damage_class_prose",
        return_value=devolver,
    )
    MDCP = files.leer_move_damage_class_prose()
    assert isinstance(MDCP, dict)
    assert len(MDCP) == 2
    assert MDCP[1][0][0] == 2
    assert MDCP[3][0][0] == 4


def test_leer_pokemon(mocker):
    files = LeerArchivos()

    devolver = {
        1: ["pikachu", 2, 3, 4, 5, 6, 7, "imagen_1"],
        2: ["Bulbasaur", 2, 3, 4, 5, 6, 7, "imagen_2"],
    }
    mocker.patch("seeds.leer_archivos.LeerArchivos.leer_pokemon", return_value=devolver)
    PK = files.leer_pokemon()
    assert PK[1][0] == "pikachu"
    assert PK[2][0] == "Bulbasaur"
    assert isinstance(PK, dict)
    assert len(PK) == 2


def test_leer_pokemon_types(mocker):
    files = LeerArchivos()
    devolver = {
        1: [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11],
        2: [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_pokemon_types", return_value=devolver
    )
    PT = files.leer_pokemon_types()
    assert isinstance(PT, dict)
    assert len(PT) == 2
    assert PT[1][0] == 1
    assert PT[2][1] == 2


def test_leer_type_names(mocker):
    files = LeerArchivos()
    devolver = {
        1: [[1, 2], ["nombre_1", "nombre_2"]],
        2: [[3, 4], ["nombre_3", "nombre_4"]],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_type_names", return_value=devolver
    )
    TN = files.leer_type_names()
    assert isinstance(TN, dict)
    assert len(TN) == 2
    assert TN[1][1][0] == "nombre_1"
    assert TN[2][1][0] == "nombre_3"


def test_leer_type_efficacy(mocker):
    files = LeerArchivos()
    devolver = {
        1: [[1, 2], [5, 8]],
        2: [[3, 4], [9, 10]],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_type_efficacy", return_value=devolver
    )
    TE = files.leer_type_efficacy()
    assert isinstance(TE, dict)
    assert len(TE) == 2
    assert TE[1][1][0] == 5
    assert TE[2][0][0] == 3


def test_leer_pokemon_stats(mocker):
    files = LeerArchivos()
    devolver = {
        1: [[0, 3, 1, 2], [1, 2, 3, 4]],
        2: [[0, 3, 1, 2], [1, 2, 3, 4]],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_pokemon_stats", return_value=devolver
    )
    PS = files.leer_pokemon_stats()
    assert isinstance(PS, dict)
    assert len(PS) == 2
    assert PS[1][0][1] == 3
    assert PS[2][1][1] == 2


def test_leer_stats(mocker):
    files = LeerArchivos()
    devolver = {
        1: [0, "stats_1", 1, 2],
        2: [0, "stats_2", 1, 2],
    }
    mocker.patch("seeds.leer_archivos.LeerArchivos.leer_stats", return_value=devolver)
    ST = files.leer_stats()
    assert isinstance(ST, dict)
    assert len(ST) == 2
    assert ST[1][1] == "stats_1"
    assert ST[2][1] == "stats_2"


def test_leer_pokemon_evolutions(mocker):
    files = LeerArchivos()
    devolver = {
        1: 4,
        2: 5,
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_pokemon_evolutions",
        return_value=devolver,
    )
    PE = files.leer_pokemon_evolutions()
    assert isinstance(PE, dict)
    assert len(PE) == 2
    assert PE[1] == 4
    assert PE[2] == 5


def test_leer_pokemon_move_methods(mocker):
    files = LeerArchivos()
    devolver = {
        1: [
            [2],
            ["hola"],
            ["descripcion"],
        ],
        3: [
            [4],
            ["hola"],
            ["descripcion"],
        ],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_pokemon_move_methods",
        return_value=devolver,
    )
    PMM = files.leer_pokemon_move_methods()
    assert isinstance(PMM, dict)
    assert len(PMM) == 2
    assert PMM[1][1][0] == "hola"
    assert PMM[3][2][0] == "descripcion"


def test_leer_pokemon_moves(mocker):
    files = LeerArchivos()
    devolver = {
        1: [[2], [3], [10], [0], [15]],
        3: [[4], [22], [16], [1], [20]],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_pokemon_moves", return_value=devolver
    )
    PM = files.leer_pokemon_moves()
    assert isinstance(PM, dict)
    assert len(PM) == 2
    assert PM[1][0][0] == 2
    assert PM[3][1][0] == 22


def test_leer_move_names(mocker):
    files = LeerArchivos()
    devolver = {
        1: [[2, 3, 4], ["hola", "hola_2"]],
        3: [[4, 5, 6], ["hola", "hola_4"]],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_move_names", return_value=devolver
    )
    MN = files.leer_move_names()
    assert isinstance(MN, dict)
    assert len(MN) == 2
    assert MN[1][0][0] == 2
    assert MN[3][1][0] == "hola"


def test_leer_move_effect_prose(mocker):
    files = LeerArchivos()

    devolver = {
        1: [1, "short_effect_1", "effect_1"],
        2: [2, "short_effect_2", "effect_2"],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_move_effect_prose", return_value=devolver
    )
    MEP = files.leer_move_effect_prose()
    assert MEP[1][1] == "short_effect_1"
    assert MEP[2][2] == "effect_2"
    assert isinstance(MEP, dict)
    assert len(MEP) == 2


def test_leer_pk_moves_clave_move_id(mocker):
    files = LeerArchivos()
    devolver = {
        5: {1: [1, 2, 3, 4]},
        6: {2: [1, 2, 3, 4]},
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_pk_moves_clave_move_id",
        return_value=devolver,
    )
    PMCMID = files.leer_pk_moves_clave_move_id()
    assert isinstance(PMCMID, dict)
    assert len(PMCMID) == 2
    assert PMCMID[5][1][0] == 1
    assert PMCMID[6][2][1] == 2


def test_leer_pokemon_types_clave_type_id(mocker):
    files = LeerArchivos()
    devolver = {
        1: [1, 2, 3, 4, 5, 5],
        2: [1, 2, 3, 4, 5],
    }
    mocker.patch(
        "seeds.leer_archivos.LeerArchivos.leer_pokemon_types_clave_type_id",
        return_value=devolver,
    )
    PTCTYPE_ID = files.leer_pokemon_types_clave_type_id()
    assert isinstance(PTCTYPE_ID, dict)
    assert len(PTCTYPE_ID) == 2
    assert PTCTYPE_ID[1][0] == 1
    assert PTCTYPE_ID[2][0] == 1
