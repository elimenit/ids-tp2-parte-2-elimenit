from pydantic import BaseModel, conint, Field  # paginacion
from typing import List, Optional  

class TipoPublic(BaseModel):
    id: int
    nombre: str

class PokemonAprendizaje(BaseModel):
    id: int
    imagen: Optional[str]
    nombre: str
    altura: float
    peso: float

class MovimientoPublicList(BaseModel):
    id: int
    nombre: str
    tipo: TipoPublic
    categoria: str
    potencia: Optional[int] = None
    precision: Optional[int] = None
    usos: int
    efecto: str

class MovimientoPublicId(MovimientoPublicList):
    pokemon_por_huevo: List[PokemonAprendizaje] = []
    pokemon_por_nivel: List[PokemonAprendizaje] = []
    pokemon_por_maquina: List[PokemonAprendizaje] = []

class FiltrosMovimientosPublic(BaseModel):
    tipo_id: Optional[int] =  Field(default=None, ge=1, le=18)
    categoria_id: Optional[int] = Field(default=None, ge=1)
    potencia_min: Optional[int] = Field(default=None, ge=1)
    potencia_max: Optional[int] = Field(default=None, ge=1)
    precision_min: Optional[int] = Field(default=None, ge=1)
    nombre: Optional[str] = None
    limit: conint(ge=1, le=100) = 50
    offset: conint(ge=0) = 0