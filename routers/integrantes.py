from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.public.equipos_public import (
    IntegranteCreate, IntegrantePublic, IntegranteUpdate,
    MovimientoPublic, MovimientoCreate
)
from dependencies.database import DatabaseDep, SessionDep
integrante_router = APIRouter(prefix="", tags=["Integrantes"])
# Integrantes
@integrante_router.post("/{equipo_id}/integrantes", status_code=201)
def add_integrante(equipo_id: int, data: IntegranteCreate, db: DatabaseDep, session: SessionDep) -> IntegrantePublic:
    return db.agreguar_integrante_equipo(session=session, equipo_id=equipo_id, intg=data)

@integrante_router.put("/{equipo_id}/integrantes/{integrante_id}")
def edit_integrante(
    equipo_id: int, integrante_id: int, data: IntegranteUpdate, db: DatabaseDep, session: SessionDep
) -> IntegrantePublic:
    return db.editar_integrante_equipo(session=session, equipo_id=equipo_id, integrante_id=integrante_id,
                                 apodo=data.apodo, movimientos=data.movimientos)

@integrante_router.delete("/{equipo_id}/integrantes/{integrante_id}")
def delete_integrante(equipo_id: int, integrante_id: int, db: DatabaseDep, session: SessionDep):
    return db.eliminar_un_integrante_equipo(session=session, equipo_id=equipo_id, integrante_id=integrante_id)

# Movimientos del integrante
@integrante_router.post("/{equipo_id}/integrantes/{integrante_id}/movimientos", status_code=201)
def add_movimiento(equipo_id: int, integrante_id: int, data: MovimientoCreate, db: DatabaseDep, session: SessionDep):
    return db.agreguar_movimientos_integrante(
        session=session, equipo_id=equipo_id,                                       
        integrante_id=integrante_id, movimiento_id=data.id_movimiento
    )
