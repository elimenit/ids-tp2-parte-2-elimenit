from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from dependencies.database import SessionDep, DatabaseDep
from models.public.pokemon_public import PokemonPublic, FilterPokemonPublic, PokemonList

router_pokemon = APIRouter(prefix="/pokemon", tags=["Pokemon"])

@router_pokemon.get("/", response_model=list[PokemonList], status_code=200)
def get_all_pokemons(  # ¡Inyectamos¡
    session: SessionDep, db: DatabaseDep,
    filters: FilterPokemonPublic = Depends()
) -> list[PokemonList]:
    return db.mostrar_todos_pokemons(session=session, filters=filters)

@router_pokemon.get("/{id}", status_code=200)
def get_one_pokemon(id: int, session: SessionDep, db: DatabaseDep):
    result = db.mostrar_un_pokemon(session, id=id) 
    if not result:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")
    return result