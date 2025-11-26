from typing import List, Optional, Dict
from sqlmodel import Session, select, func, distinct
from models.pokemon import (
    Pokemon, PokemonTipo, Tipo, TypeEfficacy, Estadistica,
    Evolucion, Movimiento, PokemonMovimiento, CategoriaMovimiento,
    EfectoMovimiento
)
from models.public.pokemon_public import FilterPokemonPublic, PokemonPublic, PokemonList
def list_pokemon(session: Session, filters: FilterPokemonPublic) -> List[PokemonList]:
    # 1. Subquery: IDs  de pokemons unicos que cumplen los filtros y ordenados
    pokemon_ids_subq = (
        select(Pokemon.id)
        .join(PokemonTipo, Pokemon.id == PokemonTipo.pokemon_id)
        .join(Tipo, Tipo.id == PokemonTipo.tipo_id)
        .distinct()
    )

    # Aplicamos filtros
    if filters.tipo is not None:
        pokemon_ids_subq = pokemon_ids_subq.where(Tipo.id == filters.tipo)
    if filters.nombre_parcial:
        pokemon_ids_subq = pokemon_ids_subq.where(func.lower(Pokemon.nombre).contains(filters.nombre_parcial.lower()))
    if filters.min_stat is not None:
        stats_sum = (
            select(Estadistica.pokemon_id,
                   (Estadistica.puntos_de_golpe + Estadistica.ataque + Estadistica.defensa +
                    Estadistica.ataque_especial + Estadistica.defensa_especial + Estadistica.velocidad)
                   .label("total")).subquery()
        )
        pokemon_ids_subq = pokemon_ids_subq.join(stats_sum, Pokemon.id == stats_sum.c.pokemon_id)
        pokemon_ids_subq = pokemon_ids_subq.where(stats_sum.c.total >= filters.min_stat)

    pokemon_ids_subq = pokemon_ids_subq.order_by(Pokemon.id)
    pokemon_ids_subq = pokemon_ids_subq.offset(filters.offset).limit(filters.limit)
    pokemon_ids_subq = pokemon_ids_subq.subquery()

    # 2. Query final: traemos solo los 20 Pokémon seleccionados y tipos
    stmt = (
        select(Pokemon, Tipo)
        .join(PokemonTipo, Pokemon.id == PokemonTipo.pokemon_id)
        .join(Tipo, Tipo.id == PokemonTipo.tipo_id)
        .join(pokemon_ids_subq, Pokemon.id == pokemon_ids_subq.c.id)
        .order_by(Pokemon.id, Tipo.id)
    )

    results = session.exec(stmt).all()
    pokemon_map: dict[int, PokemonPublic] = {}
    for pokemon, tipo in results:
        if pokemon.id not in pokemon_map:
            pokemon_map[pokemon.id] = {
                "id": pokemon.id,
                "nombre": pokemon.nombre,
                "imagen": pokemon.imagen,
                "tipos": []
            }
        pokemon_map[pokemon.id]["tipos"].append({"id": tipo.id, "nombre": tipo.nombre})

    return list(pokemon_map.values())
    
def get_pokemon(id: int, session: Session) -> Optional[dict]:
    pokemon = session.get(Pokemon, id)
    if not pokemon:
        return None

    # --- Tipos + Debilidades ---
    tipos_pokemon = session.exec(
        select(Tipo).join(PokemonTipo).where(PokemonTipo.pokemon_id == id)
    ).all()

    tipos_con_debilidades = []
    tipos_ids = [t.id for t in tipos_pokemon]

    for tipo in tipos_pokemon:
        # Buscamos que tipos son super efectivos 
        debilidades = session.exec(
            select(Tipo)
            .join(TypeEfficacy, TypeEfficacy.damage_type_id == Tipo.id)
            .where(
                TypeEfficacy.target_type_id == tipo.id,
                TypeEfficacy.damage_factor == 200
            )
        ).all()

        debilidades_list = [{"id": d.id, "nombre": d.nombre} for d in debilidades]

        tipos_con_debilidades.append({
            "id": tipo.id,
            "nombre": tipo.nombre,
            "debilidades": debilidades_list
        })

    # --- Estadísticas ---
    stats = session.get(Estadistica, id)
    estadisticas_dict = {
        "puntos_de_golpe": stats.puntos_de_golpe if stats else 0,
        "ataque": stats.ataque if stats else 0,
        "defensa": stats.defensa if stats else 0,
        "ataque_especial": stats.ataque_especial if stats else 0,
        "defensa_especial": stats.defensa_especial if stats else 0,
        "velocidad": stats.velocidad if stats else 0,
    }

    # --- Evoluciones ---
    evoluciones = session.exec(
        select(Pokemon)
        .join(Evolucion, Evolucion.to_id == Pokemon.id)
        .where(Evolucion.from_id == id)
    ).all()

    evoluciones_list = [
        {
            "id": evo.id,
            "nombre": evo.nombre,
            "imagen": evo.imagen
        }
        for evo in evoluciones
    ]

    # --- Movimientos por metodo de aprendizaje ---
    movimientos = session.exec(
        select(Movimiento, PokemonMovimiento.method_id)
        .join(PokemonMovimiento, PokemonMovimiento.move_id == Movimiento.id)
        .where(PokemonMovimiento.pokemon_id == id)
    ).all()

    por_huevo = []
    por_nivel = []
    por_maquina = []

    categoria_map = {c.id: c.nombre.lower() for c in session.exec(select(CategoriaMovimiento)).all()}
    tipo_cache = {t.id: t.nombre for t in session.exec(select(Tipo)).all()}

    for move, method_id in movimientos:
        tipo_nombre = tipo_cache.get(move.tipo_id, "Desconocido")
        cat_nombre = categoria_map.get(move.categoria_id, "status")
        nombre_efecto = session.exec(select(EfectoMovimiento).where(EfectoMovimiento.id == move.efecto_id)).first()
        move_data = {
            "id": move.id,
            "nombre": move.nombre,
            "tipo": {"id": move.tipo_id, "nombre": tipo_nombre},
            "categoria": "físico" if cat_nombre == "physical" else "especial" if cat_nombre == "special" else "estado",
            "potencia": move.potencia or 0,
            "precision": move.precision or 0,
            "usos": move.usos,
            "efecto": nombre_efecto if move.efecto_id else "Sin efecto adicional."
        }

        if method_id == 1:      # Nivel
            por_nivel.append(move_data)
        elif method_id == 2:    # Huevo
            por_huevo.append(move_data)
        elif method_id == 4:    # Maquina
            por_maquina.append(move_data)
    return {
        "id": pokemon.id,
        "nombre": pokemon.nombre,
        "imagen": pokemon.imagen,
        "altura": float(pokemon.altura) / 10,  
        "peso": float(pokemon.peso) / 10,       
        "tipos": tipos_con_debilidades,
        "estadisticas": estadisticas_dict,
        "evoluciones": evoluciones_list,
        "movimientos_huevo": por_huevo,
        "movimientos_nivel": por_nivel,
        "movimientos_maquina": por_maquina,
    }