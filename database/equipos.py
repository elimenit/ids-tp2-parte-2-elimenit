from typing import List, Optional
from sqlmodel import Session, select
from models.equipos import (
    Equipo, Integrante, IntegranteMovimiento   
)
from models.public.equipos_public import (
    EquipoCreate, EquipoList, EquipoPublic, EquipoUpdate, EquipoUpsert,
    IntegranteCreate, IntegrantePublic, IntegranteUpdate,
    MovimientoCreate, MovimientoPublic, MovimientoUpsert
)
from models.pokemon import (
    Pokemon, PokemonMovimiento, PokemonTipo,
    Movimiento, CategoriaMovimiento, EfectoMovimiento, Estadistica, 
    Evolucion
)
def show_one_team(session: Session, id: int) -> Optional[EquipoPublic]:
    equipo_db = session.get(Equipo, id)
    if not equipo_db:
        return None

    integrantes_public = []
    for integrante_db in equipo_db.integrantes:
        # 1)info pokemon
        pokemon_db = integrante_db.pokemon
        stats = session.exec(
            select(Estadistica).where(Estadistica.pokemon_id == pokemon_db.id)
        ).first()

        # 2) Tipos del pokemon
        tipos = [
            {"id": t.id, "nombre": t.nombre}
            for t in pokemon_db.tipos
        ]

        pokemon_data = {
            "id": pokemon_db.id,
            "imagen": pokemon_db.imagen,
            "nombre": pokemon_db.nombre,
            "estadisticas": {
                "ataque": stats.ataque if stats else 0,
                "defensa": stats.defensa if stats else 0,
                "ataque_especial": stats.ataque_especial if stats else 0,
                "defensa_especial": stats.defensa_especial if stats else 0,
                "puntos_de_golpe": stats.puntos_de_golpe if stats else 0,
                "velocidad": stats.velocidad if stats else 0,
            },
            "tipos": tipos,
        }

        # Movimientos del integrante
        movimientos_public = []
        for im in integrante_db.movimientos:
            mov_db = im.movimiento
            tipo = session.get(Tipo, mov_db.tipo_id)
            categoria = session.get(CategoriaMovimiento, mov_db.categoria_id)
            efecto = session.get(EfectoMovimiento, mov_db.efecto_id)

            mov_public = MovimientoPublic(
                id=mov_db.id,
                nombre=mov_db.nombre,
                tipo={"id": tipo.id, "nombre": tipo.nombre},
                categoria=categoria.nombre.lower(), 
                potencia=mov_db.potencia,
                precision=mov_db.precision,
                usos=mov_db.usos,
                efecto=efecto.efecto if efecto else ""
            )
            movimientos_public.append(mov_public)

        integrante_public = IntegrantePublic(
            id=integrante_db.id,
            apodo=integrante_db.apodo,
            pokemon=pokemon_data,
            movimientos=movimientos_public
        )
        integrantes_public.append(integrante_public)

    return EquipoPublic(
        id=equipo_db.id,
        nombre=equipo_db.nombre,
        integrantes=integrantes_public
    )