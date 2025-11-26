from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, conint

class TipoConDebilidad(BaseModel):
    id: int
    nombre: str
    debilidades: List[Dict[str, Any]]

class MovimientoPublic(BaseModel):
    id: int
    nombre: str
    tipo: Dict[str, Any]
    categoria: str
    potencia: int
    precision: int
    usos: int
    efecto: str

class EvolucionPublic(BaseModel):
    id: int
    nombre: str
    imagen: str
class PokemonList(BaseModel):
    id: int
    nombre: str
    imagen: str
    tipos: list

class PokemonPublic(BaseModel):
    id: int
    nombre: str
    imagen: str
    altura: float
    peso: float
    tipos: List[TipoConDebilidad]
    estadisticas: Dict[str, int]
    evoluciones: List[EvolucionPublic]
    movimientos_huevo: List[MovimientoPublic]
    movimientos_nivel: List[MovimientoPublic]
    movimientos_maquina: List[MovimientoPublic]

class FilterPokemonPublic(BaseModel):
    tipo: Optional[int] = Field(default=None, ge=1, le=18)
    nombre_parcial: Optional[str] = Field(default=None, min_length=2)
    min_stat: Optional[int] = Field(default=None, ge=0)
    limit: conint(ge=1, le=100) =50    # máximo 100 por página
    offset: conint(ge=0) = 0