from sqlmodel import Session, select
from typing import List, Optional
from models.public.movimiento_public import (
    TipoPublic, MovimientoPublicId, MovimientoPublicList, 
    FiltrosMovimientosPublic, PokemonAprendizaje
)
from models.pokemon import (
    Pokemon, PokemonMovimiento, PokemonTipo,
    Movimiento, EfectoMovimiento, CategoriaMovimiento,
    Tipo
)
from fastapi import HTTPException

def show_one_move(session: Session, move_id: int) -> MovimientoPublicId:
    movimiento = session.get(Movimiento, move_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    tipo = session.get(Tipo, movimiento.tipo_id)
    categoria = session.get(CategoriaMovimiento, movimiento.categoria_id)
    efecto = session.get(EfectoMovimiento, movimiento.efecto_id)

    if not tipo or not categoria or not efecto:
        raise HTTPException(status_code=500, detail="Datos corruptos en el movimiento")

    statement = (
        select(Pokemon, PokemonMovimiento.method_id)
        .join(PokemonMovimiento, Pokemon.id == PokemonMovimiento.pokemon_id)
        .where(PokemonMovimiento.move_id == move_id)
        .group_by(Pokemon.id, PokemonMovimiento.method_id) 
    )

    resultados = session.exec(statement).all()

    por_huevo = []
    por_nivel = []
    por_maquina = []

    for pokemon, method_id in resultados:
        pokemon_aprendizaje = PokemonAprendizaje(
            id=pokemon.id,
            nombre=pokemon.nombre,
            imagen=pokemon.imagen,
            altura=pokemon.altura,
            peso=pokemon.peso,
        )
        
        if method_id == 1:
            por_nivel.append(pokemon_aprendizaje)
        elif method_id == 2:
            por_huevo.append(pokemon_aprendizaje)
        elif method_id == 4:
            por_maquina.append(pokemon_aprendizaje)

    return MovimientoPublicId(
        id=movimiento.id,
        nombre=movimiento.nombre,
        tipo=TipoPublic(id=tipo.id, nombre=tipo.nombre),
        categoria=categoria.nombre.lower(),
        potencia=movimiento.potencia,
        precision=movimiento.precision,
        usos=movimiento.usos,
        efecto=efecto.efecto,
        pokemon_por_huevo=por_huevo,
        pokemon_por_nivel=por_nivel,
        pokemon_por_maquina=por_maquina,
    )
def show_all_moves(session: Session, filtros: FiltrosMovimientosPublic) -> List[MovimientoPublicList]:
    query = (
        select(
            Movimiento.id,
            Movimiento.nombre,
            Movimiento.potencia,
            Movimiento.precision,
            Movimiento.usos,
            Tipo.id.label("tipo_id"),
            Tipo.nombre.label("tipo_nombre"),
            CategoriaMovimiento.nombre.label("cat_nombre"),
            EfectoMovimiento.efecto.label("efecto_texto"),
        )
        .join(Tipo, Movimiento.tipo_id == Tipo.id)
        .join(CategoriaMovimiento, Movimiento.categoria_id == CategoriaMovimiento.id)
        .join(EfectoMovimiento, Movimiento.efecto_id == EfectoMovimiento.id)
    )

    # Aplicar filtros de forma secuencial
    if filtros.tipo_id:
        query = query.where(Movimiento.tipo_id == filtros.tipo_id)
    
    if filtros.categoria_id:
        query = query.where(Movimiento.categoria_id == filtros.categoria_id)
    
    if filtros.nombre:
        query = query.where(Movimiento.nombre.ilike(f"%{filtros.nombre}%"))

    query = query.offset(filtros.offset).limit(filtros.limit).order_by(Movimiento.id)

    resultados = session.exec(query).all()

    return [
        MovimientoPublicList(     
            id=row.id,
            nombre=row.nombre,
            tipo=TipoPublic(id=row.tipo_id, nombre=row.tipo_nombre),
            categoria=row.cat_nombre.lower(),
            potencia=row.potencia,
            precision=row.precision,
            usos=row.usos,
            efecto=row.efecto_texto,
        )
        for row in resultados
    ]