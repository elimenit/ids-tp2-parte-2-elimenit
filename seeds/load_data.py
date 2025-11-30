from typing import Optional
from sqlmodel import SQLModel, Session, select
from models.pokemon import (
    CategoriaMovimiento,
    EfectoMovimiento,
    Estadistica,
    Evolucion,
    Movimiento,
    Pokemon,
    PokemonMovimiento,
    PokemonTipo,
    Tipo,
    TypeEfficacy
)
from dependencies.database import engine

def zero_if_empty(value: str) -> Optional[int]:
    return int(value) if value else 0

def carguar_tipos(session: Session) -> None:
    f =  open("data/type_names.csv", "r")
    f.readline()
    linea = f.readline()
    while linea:
        partes = linea.rstrip("\n").split(",")
        local_lenguaje_id = int(partes[1])
        if local_lenguaje_id == 7:
            type_id = int(partes[0])
            name = partes[2]
            session.add(Tipo(id=type_id, nombre=name))
        linea=f.readline()
    f.close()
    session.commit()

def carguar_type_efficacy(session: Session) -> None:
    f = open("data/type_efficacy.csv",'r')
    f.readline()
    linea = f.readline()
    while linea:
        partes = linea.rstrip("\n").split(",")
        session.add(
            TypeEfficacy(
                damage_type_id=int(partes[0]),
                target_type_id=int(partes[1]),
                damage_factor=int(partes[2]),
            )
        )
        linea = f.readline()
    f.close()
    session.commit()

def carguar_pokemon(session:Session) -> None:
    f = open("data/pokemon.csv", 'r')
    f.readline()
    linea = f.readline()
    while linea:
        partes = linea.rstrip("\n").split(',')
        session.add(
            Pokemon(
                id=int(partes[0]),
                nombre=partes[1],
                imagen = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{str(partes[0])}.png",
                species_id=int(partes[2]),
                altura=int(partes[3]),
                peso=int(partes[4]),
                base_experience=int(partes[5]),
            )
        )
        linea = f.readline()
    f.close()
    session.commit()
    

def carguar_pokemon_types(session: Session) -> None:
    f = open("data/pokemon_types.csv", 'r')
    f.readline()
    linea = f.readline()
    while linea:
        partes = linea.rstrip("\n").split(",")
        session.add(
            PokemonTipo(
                pokemon_id=int(partes[0]),
                tipo_id=int(partes[1]),
                slot=int(partes[2]),
            )
        )
        linea = f.readline()
    f.close()
    session.commit()

def carguar_pokemon_stats(session: Session) -> None:
    f = open("data/pokemon_stats.csv", 'r')
    f.readline()
    linea = f.readline()
    i = 1
    temporal = {}
    while linea:
        partes = linea.rstrip("\n").split(',')
        if i < 6:
            temporal[0] = int(partes[0])
            partes[2] = int(partes[2])
            match int(partes[1]):
                case 1:
                    temporal[1] = partes[2]
                case 2: 
                    temporal[2] = partes[2]
                case 3:
                    temporal[3] = partes[2]
                case 4:
                    temporal[4] = partes[2]
                case 5:
                    temporal[5] = partes[2]
                # Nunca va ha lleguar al case 6:
            i += 1
        else:
            temporal[6] = int(partes[2])
            session.add(
                Estadistica(
                    pokemon_id=temporal[0],
                    puntos_de_golpe=temporal[1],
                    ataque=temporal[2],
                    defensa=temporal[3],
                    ataque_especial=temporal[4],
                    defensa_especial=temporal[5],
                    velocidad=temporal[6]    
                )
            )
            i = 1
            temporal = {}
        linea = f.readline()
    f.close()
    session.commit()

def carguar_pokemon_evolutions(session:Session) -> None:
    f = open("data/pokemon_evolutions.csv")
    f.readline()
    linea = f.readline()
    while linea:
        partes = linea.rstrip("\n").split(",")
        session.add(
            Evolucion(
                from_id=int(partes[0]),
                to_id=int(partes[1])
            )
        )
        linea= f.readline()
    f.close()
    session.commit()

def carguar_move_damage_class_prose(session: Session) -> None:
    f = open("data/move_damage_class_prose.csv", 'r')
    f.readline()
    linea = f.readline()
    while linea:
        partes = linea.rstrip("\n").split(",")
        if int(partes[1]) == 7: #local_lenguaje_id = 7
            session.add(CategoriaMovimiento(id=int(partes[0]), nombre=partes[2]))
        linea = f.readline()
    
    f.close()
    session.commit()

def carguar_efectos_movimiento(session: Session) -> None:
    f = open("data/move_effect_prose.csv", 'r')
    f.readline()
    linea = f.readline()
    while linea:
        partes = linea.rstrip("\n").split(",",3)
        if len(partes) == 4:
            try:
                partes[1] = int(partes[1])
                print(f"funciona {partes[0]} y {partes[1]} con el efecto {partes[2]}")
                session.add(EfectoMovimiento(id=int(partes[0]), efecto=partes[2]))
            except Exception as e:
                pass
        linea = f.readline()
    f.close()
    session.commit()

def carguar_moves(session: Session) -> None:
    move_names= {}
    g = open("data/move_names.csv")
    g.readline()
    linea_pong = g.readline()
    while linea_pong:
        partes = linea_pong.rstrip("\n").split(",")
        if int(partes[1]) == 7:
            move_names[int(partes[0])] = partes[2]
        linea_pong = g.readline()
    g.close()

    f = open("data/moves.csv")
    f.readline()
    linea = f.readline()
    while linea:
        partes = linea.rstrip("\n").split(",")
        if partes[0]:
            session.add(
                Movimiento(
                    id=int(partes[0]),
                    nombre=move_names.get(int(partes[0]), "default"),
                    tipo_id=int(partes[3]),
                    potencia=zero_if_empty(partes[4]),
                    usos=zero_if_empty(partes[5]),
                    precision=zero_if_empty(partes[6]),
                    priority=int(partes[7]),
                    target_id=int(partes[8]),
                    categoria_id=int(partes[9]),
                    efecto_id=int(partes[10]),
                    efecto_chance=zero_if_empty(partes[11]),
                )
            )
        linea = f.readline()
    f.close()
    session.commit()
    

def carguar_pokemon_moves(session: Session) -> None:
    f = open("data/pokemon_moves.csv",'r')
    f.readline()
    linea = f.readline()
    while linea:              
        partes = linea.rstrip("\n").split(",")
        session.add(
            PokemonMovimiento(
                pokemon_id=int(partes[0]),
                move_id=int(partes[2]),
                method_id=int(partes[3]),
            )
        )
        linea = f.readline()
    f.close()
    session.commit()

def load_data(session: Session) -> None:
    if session.exec(select(Pokemon)).first():
        print("Base de datos ya cargada.")
        return None
    
    carguar_tipos(session)
    carguar_type_efficacy(session)
    carguar_pokemon(session)
    carguar_pokemon_types(session)
    carguar_pokemon_stats(session)
    carguar_pokemon_evolutions(session)
    carguar_move_damage_class_prose(session)
    carguar_efectos_movimiento(session)
    carguar_moves(session)
    carguar_pokemon_moves(session)
    print("Datos cargados exitosamente.")

def carguar_models_pokemon_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        load_data(session)