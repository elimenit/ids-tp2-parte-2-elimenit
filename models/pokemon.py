from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

class PokemonTipo(SQLModel, table=True):
    __tablename__ = "pokemon_tipo"
    
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    tipo_id: int = Field(foreign_key="tipo.id", primary_key=True)
    slot: int = Field(default=1) 

class Tipo(SQLModel, table=True):
    __tablename__ = "tipo"
    
    id: int = Field(primary_key=True)
    nombre: str = Field(index=True, unique=True)
    
    # Relación inversa: un tipo tiene muchos pokemons
    pokemons: List["Pokemon"] = Relationship(
        back_populates="tipos",
        link_model=PokemonTipo  
    )

class Pokemon(SQLModel, table=True):
    __tablename__ = "pokemon"
    
    id: int = Field(primary_key=True)
    nombre: str = Field(index=True)
    species_id: int
    altura: float
    peso: float
    base_experience: int
    imagen: Optional[str] = Field(default=None)
    # Relación muchos-a-muchos con Tipo (solo aquí usamos link_model)
    tipos: List[Tipo] = Relationship(
        back_populates="pokemons",
        link_model=PokemonTipo
    )


class TypeEfficacy(SQLModel, table=True):
    __tablename__ = "type_efficacy"
    
    damage_type_id: int = Field(foreign_key="tipo.id", primary_key=True)
    target_type_id: int = Field(foreign_key="tipo.id", primary_key=True)
    damage_factor: int = Field()

class Estadistica(SQLModel, table=True):
    __tablename__ = "estadistica"
    
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    puntos_de_golpe: int
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    velocidad: int


class Evolucion(SQLModel, table=True):
    __tablename__ = "evolucion"
    
    from_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    to_id: int = Field(foreign_key="pokemon.id", primary_key=True)

class CategoriaMovimiento(SQLModel, table=True):
    __tablename__ = "categoria_movimiento"
    
    id: int = Field(primary_key=True)
    nombre: str = Field(unique=True)  # Physical, Special, Status


class EfectoMovimiento(SQLModel, table=True):
    __tablename__ = "efecto_movimiento"
    
    id: int = Field(primary_key=True)
    efecto: str


class Movimiento(SQLModel, table=True):
    __tablename__ = "movimiento"
    
    id: int = Field(primary_key=True)
    nombre: str = Field(index=True)
    #generation_id: int
    tipo_id: int = Field(foreign_key="tipo.id")
    
    potencia: Optional[int] = None
    usos: int  # PP
    precision: Optional[int] = Field(default=None, alias="precision")  # 'precision' a veces da conflicto
    priority: int = Field(default=0)
    target_id: int
    categoria_id: int = Field(foreign_key="categoria_movimiento.id")
    efecto_id: int = Field(foreign_key="efecto_movimiento.id")
    efecto_chance: Optional[int] = None  

class PokemonMovimiento(SQLModel, table=True):
    __tablename__ = "pokemon_movimiento"
    
    id: Optional[int] = Field(default=None, primary_key=True) 
    
    pokemon_id: int = Field(foreign_key="pokemon.id", index=True)
    #version_group_id: int = Field(index=True)
    move_id: int = Field(foreign_key="movimiento.id", index=True)
    method_id: int