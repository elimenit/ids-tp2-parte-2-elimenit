from models.public.pokemon_public import PokemonPublic, FilterPokemonPublic, PokemonList
from models.public.movimiento_public import (
    MovimientoPublicId,
    MovimientoPublicList,
    FiltrosMovimientosPublic,
)
from models.public.equipos_public import (
    EquipoPublic,
    EquipoCreate,
    EquipoUpdate,
    EquipoList,
    IntegrantePublic,
    IntegranteCreate,
    IntegranteUpdate,
    MovimientoCreate,
    MovimientoPublic,
    FiltrosEQuiposPublic,
    FiltrosIntegrantePublic,
)
from fastapi import HTTPException
from database.pokemon import list_pokemon, get_pokemon
from database.movimientos import show_one_move, show_all_moves
from models.pokemon import (
    Estadistica,
    Movimiento,
    CategoriaMovimiento,
    EfectoMovimiento,
    Pokemon,
    PokemonMovimiento,
    PokemonTipo,
    Tipo,
)

from models.equipos import Equipo, Integrante, IntegranteMovimiento
from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select, func, delete
from typing import List, Optional


class Database:
    #  ==================== POKEMON ====================
    def mostrar_un_pokemon(
        self,
        session: Session,
        id: int,
        tipo: int = None,
        nombre_parcial: str = "",
        min_stat: int = None,
    ) -> PokemonPublic:
        return get_pokemon(id=id, session=session)

    def mostrar_todos_pokemons(  #
        self, session: Session, filters: FilterPokemonPublic
    ) -> List[PokemonList]:
        return list_pokemon(session=session, filters=filters)

    # ==================== MOVIMIENTOS ====================
    def mostrar_un_movimiento(self, session: Session, id: int) -> MovimientoPublicId:
        return show_one_move(session=session, move_id=id)

    def mostrar_todos_movimientos(
        self, session: Session, filtros: FiltrosMovimientosPublic
    ) -> List[MovimientoPublicList]:
        return show_all_moves(session, filtros)

    # ==================== EQUIPOS ====================
    def mostrar_un_equipo(self, session: Session, id: int) -> Optional[EquipoPublic]:
        equipo = session.get(Equipo, id)
        if not equipo:
            return None

        integrantes_public = []
        for integrante in equipo.integrantes:
            pokemon = integrante.pokemon
            stats = session.exec(
                select(Estadistica).where(Estadistica.pokemon_id == pokemon.id)
            ).one()

            tipos = [{"id": t.id, "nombre": t.nombre} for t in pokemon.tipos]

            pokemon_data = {
                "id": pokemon.id,
                "imagen": pokemon.imagen,
                "nombre": pokemon.nombre,
                "estadisticas": {
                    "ataque": stats.ataque,
                    "defensa": stats.defensa,
                    "ataque_especial": stats.ataque_especial,
                    "defensa_especial": stats.defensa_especial,
                    "puntos_de_golpe": stats.puntos_de_golpe,
                    "velocidad": stats.velocidad,
                },
                "tipos": tipos,
            }

            movimientos_public = []
            for im in integrante.movimientos:
                mov = im.movimiento
                tipo = session.get(Tipo, mov.tipo_id)
                cat = session.get(CategoriaMovimiento, mov.categoria_id)
                efecto = session.get(EfectoMovimiento, mov.efecto_id)

                movimientos_public.append(
                    MovimientoPublic(
                        id=mov.id,
                        nombre=mov.nombre,
                        tipo={"id": tipo.id, "nombre": tipo.nombre},
                        categoria=cat.nombre.lower(),
                        potencia=mov.potencia,
                        precision=mov.precision,
                        usos=mov.usos,
                        efecto=efecto.efecto if efecto else "",
                    )
                )

            integrantes_public.append(
                IntegrantePublic(
                    id=integrante.id,
                    apodo=integrante.apodo,
                    pokemon=pokemon_data,
                    movimientos=movimientos_public,
                )
            )

        return EquipoPublic(
            id=equipo.id, nombre=equipo.nombre, integrantes=integrantes_public
        )

    def mostrar_todos_equipos(
        self, session: Session, filtros: FiltrosEQuiposPublic
    ) -> list[EquipoList]:
        equipos = session.exec(select(Equipo)).all()
        count_integrantes = select(func.count(Integrante.id)).where(
            Integrante.equipo_id == Equipo.id
        )
        query = (
            select(
                Equipo.id, Equipo.nombre, count_integrantes.label("cant_integrantes")
            )
            .offset(filtros.offset)
            .limit(filtros.limit)
            .order_by(Equipo.id)
        )
        if filtros.id is not None:
            query = query.where(Equipo.id == filtros.id)
        if filtros.nombre_parcial:
            query = query.where(
                func.lower(Equipo.nombre).contains(filtros.nombre_parcial.strip())
            )
        query.order_by(Equipo.id)
        resultados = session.exec(query).all()
        return [
            EquipoList(
                id=row.id, nombre=row.nombre, cant_integrantes=row.cant_integrantes or 0
            )
            for row in resultados
        ]

    def agreguar_un_equipo(self, session: Session, nombre: str) -> EquipoPublic:
        if session.exec(select(Equipo).where(Equipo.nombre == nombre)).first():
            raise HTTPException(
                detail="Ya existe un equipo con ese mismo nombre", status_code=400
            )
        nuevo = Equipo(nombre=nombre)
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        return EquipoPublic(id=nuevo.id, nombre=nuevo.nombre, integrantes=[])

    def editar_un_equipo(self, session: Session, id: int, nombre: str) -> EquipoPublic:
        equipo = session.get(Equipo, id)
        if not equipo:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        equipo.nombre = nombre
        session.add(equipo)
        session.commit()
        session.refresh(equipo)
        return self.mostrar_un_equipo(session=session, id=id)

    def eliminar_un_equipo(self, session: Session, id: int) -> EquipoPublic:
        equipo = session.get(Equipo, id)
        if not equipo:
            raise HTTPException(
                status_code=404, detail="Equipo no encontrado o no existente"
            )
        if equipo.integrantes:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar el equipo porque tiene integrantes asignados. "
                "Primero reasigna o elimina los integrantes.",
            )
        equipo_viejo = self.mostrar_un_equipo(session=session, id=id)
        session.delete(equipo)
        session.commit()
        return equipo_viejo

    # ==================== INTEGRANTES ====================
    def agreguar_integrante_equipo(
        self, equipo_id: int, session: Session, intg: IntegranteCreate
    ) -> IntegrantePublic:
        pokemon = session.get(Pokemon, intg.id_pokemon)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon no existe")

        nuevo = Integrante(
            equipo_id=equipo_id, pokemon_id=intg.id_pokemon, apodo=intg.apodo
        )
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        return self._integrante_to_public(session, nuevo)

    def editar_integrante_equipo(
        self,
        session: Session,
        equipo_id: int,
        integrante_id: int,
        apodo: Optional[str] = None,
        movimientos: Optional[List[int]] = None,
    ) -> IntegrantePublic:
        integrante = session.get(Integrante, integrante_id)
        if not integrante or integrante.equipo_id != equipo_id:
            raise HTTPException(status_code=404, detail="Integrante no encontrado")

        if apodo is not None:
            integrante.apodo = apodo

        if movimientos is not None:
            session.exec(
                delete(IntegranteMovimiento).where(
                    IntegranteMovimiento.integrante_id == integrante_id
                )
            )
            for mov_id in movimientos:
                session.add(
                    IntegranteMovimiento(
                        integrante_id=integrante_id, movimiento_id=mov_id
                    )
                )

        session.add(integrante)
        session.commit()
        session.refresh(integrante)
        return self._integrante_to_public(session, integrante)

    def eliminar_un_integrante_equipo(
        self, session: Session, equipo_id: int, integrante_id: int
    ) -> IntegrantePublic:
        integrante = session.get(Integrante, integrante_id)
        if not integrante or integrante.equipo_id != equipo_id:
            raise HTTPException(status_code=404, detail="Integrante no encontrado")

        public = self._integrante_to_public(session, integrante)
        session.delete(integrante)
        session.commit()
        return public

    def agreguar_movimientos_integrante(
        self, session: Session, equipo_id: int, integrante_id: int, movimiento_id: int
    ) -> MovimientoPublic:
        integrante = session.get(Integrante, integrante_id)
        if not integrante or integrante.equipo_id != equipo_id:
            raise HTTPException(
                status_code=404, detail="Integrante no pertenece al equipo"
            )

        mov = session.get(Movimiento, movimiento_id)
        if not mov:
            raise HTTPException(status_code=404, detail="Movimiento no existe")

        existe = session.exec(
            select(IntegranteMovimiento).where(
                IntegranteMovimiento.integrante_id == integrante_id,
                IntegranteMovimiento.movimiento_id == movimiento_id,
            )
        ).first()
        if existe:
            raise HTTPException(
                status_code=404, detail="El movimiento ya está asignado"
            )

        session.add(
            IntegranteMovimiento(
                integrante_id=integrante_id, movimiento_id=movimiento_id
            )
        )
        session.commit()

        tipo = session.get(Tipo, mov.tipo_id)
        cat = session.get(CategoriaMovimiento, mov.categoria_id)
        efecto = session.get(EfectoMovimiento, mov.efecto_id)

        return MovimientoPublic(
            id=mov.id,
            nombre=mov.nombre,
            tipo={"id": tipo.id, "nombre": tipo.nombre},
            categoria=cat.nombre.lower(),
            potencia=mov.potencia,
            precision=mov.precision,
            usos=mov.usos,
            efecto=efecto.efecto if efecto else "",
        )

    # ==================== HELPER PRIVADO ====================
    def _integrante_to_public(
        self, session: Session, integrante: Integrante
    ) -> IntegrantePublic:
        pokemon = integrante.pokemon
        stats = session.exec(
            select(Estadistica).where(Estadistica.pokemon_id == pokemon.id)
        ).one()

        tipos = [{"id": t.id, "nombre": t.nombre} for t in pokemon.tipos]

        pokemon_data = {
            "id": pokemon.id,
            "imagen": pokemon.imagen,
            "nombre": pokemon.nombre,
            "estadisticas": {
                "ataque": stats.ataque,
                "defensa": stats.defensa,
                "ataque_especial": stats.ataque_especial,
                "defensa_especial": stats.defensa_especial,
                "puntos_de_golpe": stats.puntos_de_golpe,
                "velocidad": stats.velocidad,
            },
            "tipos": tipos,
        }

        movimientos_public = []
        for im in integrante.movimientos:
            mov = im.movimiento
            tipo = session.get(Tipo, mov.tipo_id)
            cat = session.get(CategoriaMovimiento, mov.categoria_id)
            efecto = session.get(EfectoMovimiento, mov.efecto_id)

            movimientos_public.append(
                MovimientoPublic(
                    id=mov.id,
                    nombre=mov.nombre,
                    tipo={"id": tipo.id, "nombre": tipo.nombre},
                    categoria=cat.nombre.lower(),
                    potencia=mov.potencia,
                    precision=mov.precision,
                    usos=mov.usos,
                    efecto=efecto.efecto if efecto else "",
                )
            )

        return IntegrantePublic(
            id=integrante.id,
            apodo=integrante.apodo,
            pokemon=pokemon_data,
            movimientos=movimientos_public,
        )
