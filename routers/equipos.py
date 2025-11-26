from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlmodel import Session
from dependencies.database import DatabaseDep, SessionDep
from models.public.equipos_public import (
    EquipoPublic, EquipoList, EquipoCreate, EquipoUpdate,
    FiltrosEQuiposPublic
)
from routers.integrantes import integrante_router

team_router = APIRouter(prefix="/equipos", tags=["Equipos"])
team_router.include_router(integrante_router)

@team_router.get("/{equipo_id}", )
def get_equipo(equipo_id: int, db: DatabaseDep, session: SessionDep) -> Optional[EquipoPublic]:
    return db.mostrar_un_equipo(session=session, id=equipo_id)

@team_router.get("/", status_code=200)
def list_equipos(db: DatabaseDep, session: SessionDep, filtros: FiltrosEQuiposPublic = Depends())-> List[EquipoList]:
    return db.mostrar_todos_equipos(session=session, filtros=filtros)

@team_router.post("/", status_code=201)
def create_equipo(data: EquipoCreate, db: DatabaseDep, session: SessionDep) ->EquipoPublic:
    return db.agreguar_un_equipo(session=session, nombre=data.nombre)

@team_router.put("/{equipo_id}")
def update_equipo(equipo_id: int, data: EquipoUpdate, db: DatabaseDep, session: SessionDep) -> EquipoPublic:
    return db.editar_un_equipo(session=session, id=equipo_id, nombre=data.nombre)

@team_router.delete("/{equipo_id}")
def delete_equipo(equipo_id: int, db: DatabaseDep, session: SessionDep) -> EquipoPublic:
    return db.eliminar_un_equipo(session=session, id=equipo_id)

