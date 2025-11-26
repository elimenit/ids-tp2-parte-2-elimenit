from sqlmodel import create_engine, Session
from typing import Annotated, Generator
from fastapi import Depends
from database.database_public import Database
engine = create_engine("sqlite:///database.db", echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

database_instance = Database()
def get_database() -> Database:
    global database_instance
    if database_instance is None:
        raise RuntimeError("Database instance not inicialized")
    return database_instance

DatabaseDep = Annotated[Database, Depends(get_database)]
SessionDep = Annotated[Session, Depends(get_session)]