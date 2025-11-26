from pydantic import BaseModel, Field, conint
from typing import List, Optional
# Movimientos
class MovimientoPublic(BaseModel):
    id: int
    nombre: str
    tipo: dict                      # ← { "id": 10, "nombre": "Fuego" }
    categoria: str
    potencia: Optional[int] = None
    precision: Optional[int] = None
    usos: int
    efecto: str

class MovimientoCreate(BaseModel):
    id_movimiento: int

class MovimientoUpsert(BaseModel):
    id: int = Field(gt=0)

class IntegranteCreate(BaseModel):
    id_pokemon: int
    apodo: Optional[str] = None


class IntegranteUpdate(BaseModel):
    apodo: Optional[str] = None
    movimientos: Optional[List[int]] = None  

class IntegrantePublic(BaseModel):
    id: int
    apodo: Optional[str] = None
    pokemon: dict                    
    movimientos: List[MovimientoPublic] = []

# Equipo
class EquipoCreate(BaseModel):
    nombre: str

class EquipoUpsert(BaseModel):
    id: int

class EquipoUpdate(BaseModel):
    nombre: str

class EquipoPublic(BaseModel):
    id: int
    nombre: str
    integrantes: List[IntegrantePublic] = []

class EquipoList(BaseModel):
    id: int
    nombre: str
    cant_integrantes: int

class FiltrosIntegrantePublic(BaseModel):
    id: Optional[int] = Field(default=None, ge=1)
    nombre_parcial: Optional[str] = Field(default=None, min_length=2)
    limit: conint(ge=1, le=100) = 50
    offset: conint(ge=0) = 0

class FiltrosEQuiposPublic(BaseModel):
    id: Optional[int] = Field(default=None, ge=1)
    nombre_parcial: Optional[str] = Field(default=None, min_length=2)
    limit: conint(ge=1, le=100) = 50
    offset: conint(ge=0) = 0