from dependencies.database import DatabaseDep, SessionDep
from fastapi import APIRouter, Depends
from models.public.movimiento_public import(
    FiltrosMovimientosPublic, MovimientoPublicList,
    MovimientoPublicId
)
from typing import List

move_router = APIRouter(prefix="/movimientos", tags=["Movimientos"])

@move_router.get("/{id}", response_model=MovimientoPublicId, status_code=200)
def show_one_move(id: int, db: DatabaseDep, session: SessionDep):
    return db.mostrar_un_movimiento(session, id)

@move_router.get("/", response_model=list[MovimientoPublicList], status_code=200)
def show_all_moves(db: DatabaseDep, session: SessionDep, filtros = Depends(FiltrosMovimientosPublic)):
    return db.mostrar_todos_movimientos(session, filtros)

