from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session
from pydantic import BaseModel
from typing import List
from models.pokemon import (
    Pokemon, PokemonMovimiento, PokemonTipo,
    Movimiento
)

# ==================== EQUIPOS Y INTEGRANTES ====================

class Equipo(SQLModel, table=True):
    __tablename__ = "equipo"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)

    integrantes: List["Integrante"] = Relationship(back_populates="equipo")


class Integrante(SQLModel, table=True):
    __tablename__ = "integrante"

    id: Optional[int] = Field(default=None, primary_key=True)
    equipo_id: int = Field(foreign_key="equipo.id", ondelete="CASCADE")  # Cuando elimine equipe
    pokemon_id: int = Field(foreign_key="pokemon.id")
    apodo: Optional[str] = None

    equipo: Optional[Equipo] = Relationship(back_populates="integrantes")
    pokemon: Optional[Pokemon] = Relationship()
    movimientos: List["IntegranteMovimiento"] = Relationship(
        back_populates="integrante",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}  # ayuda -> delete cascada
    )

class IntegranteMovimiento(SQLModel, table=True):
    __tablename__ = "integrante_movimiento"

    integrante_id: int = Field(foreign_key="integrante.id", primary_key=True)
    movimiento_id: int = Field(foreign_key="movimiento.id", primary_key=True)

    integrante: Integrante = Relationship(back_populates="movimientos")
    movimiento: Movimiento = Relationship()